package bot

import (
	"log"
	"unicode"
	"mybot/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Bot struct {
	botAPI     tgbotapi.BotAPI
	updateCfg  tgbotapi.UpdateConfig
	updateChan <-chan tgbotapi.Update

	orderMap map[int64][]fsm.UserOrder

	TRANSITION_TABLE []fsm.MessageHandlers
}

func (bot *Bot) Init(token string) {
	botAPIPtr, err := tgbotapi.NewBotAPI(token)

	if err != nil {
		log.Panic("Error: bot init is failed", err)
	}

	bot.botAPI = *botAPIPtr
	bot.orderMap = make(map[int64][]fsm.UserOrder)

	bot.TRANSITION_TABLE = []fsm.MessageHandlers{
		func(order *fsm.UserOrder, msg tgbotapi.Message) {
			bot.HandleNameMessage(order, msg)
		},
		func(order *fsm.UserOrder, msg tgbotapi.Message) {
			bot.HandleAmountMessage(order, msg)
		},
		func(order *fsm.UserOrder, msg tgbotapi.Message) {
			bot.HandleConfirmingMessage(order, msg)
		}}
}

func (bot *Bot) SetUpdate(offset int, timeout int) {
	bot.updateCfg = tgbotapi.NewUpdate(offset)
	bot.updateCfg.Timeout = timeout
}

func (bot *Bot) StartListen() {
	bot.updateChan = bot.botAPI.GetUpdatesChan(bot.updateCfg)
}

func (bot *Bot) ProcessOrders() {
    for update := range bot.updateChan {
        if update.Message == nil {
            continue
        }

        userMsg := update.Message
        chatID := userMsg.Chat.ID

        if userMsg.IsCommand() && userMsg.Command() == "start" {
            newOrder := fsm.UserOrder{CurState: fsm.WAITING_NAME}
            bot.orderMap[chatID] = append(bot.orderMap[chatID], newOrder)

            botMsg := tgbotapi.NewMessage(chatID, "Enter the name of good")
            botMsg.ReplyToMessageID = userMsg.MessageID
            bot.botAPI.Send(botMsg)
            continue
        }

        orders, exists := bot.orderMap[chatID]
        if !exists || len(orders) == 0 {
            botMsg := tgbotapi.NewMessage(chatID, "Please send /start to create a new order.")
            bot.botAPI.Send(botMsg)
            continue
        }

        lastIdx := len(orders) - 1
        currentOrder := &bot.orderMap[chatID][lastIdx]

        if currentOrder.CurState == fsm.SUCCESS {
            msgText := "Your order is done. Write command /start for new order"
            botMsg := tgbotapi.NewMessage(chatID, msgText)
            botMsg.ReplyToMessageID = userMsg.MessageID
            bot.botAPI.Send(botMsg)
            continue
        }

        stateFunc := bot.TRANSITION_TABLE[currentOrder.CurState]
        stateFunc(currentOrder, *userMsg)

        log.Printf("User %d moved to state: %v", chatID, currentOrder.CurState)
    }
}

func (bot *Bot) HandleConfirmingMessage(order *fsm.UserOrder, msg tgbotapi.Message) {
	if msg.Text != "Y" && msg.Text != "N" {
		return
	}

	order.IsConfirm = msg.Text == "Y"
	order.CurState = fsm.SUCCESS

	botMsg := tgbotapi.NewMessage(msg.Chat.ID, "Order is done")
	botMsg.ReplyToMessageID = msg.MessageID

	_, err := bot.botAPI.Send(botMsg)
	if err != nil {
		log.Printf("Ошибка при отправке сообщения: %v", err)
	}
}

func (bot *Bot) HandleAmountMessage(order *fsm.UserOrder, msg tgbotapi.Message) {
	log.Printf("В функции запроса суммы")

	if len(msg.Text) == 0 {
		return
	}

	for _, ch := range msg.Text {
		if !unicode.IsDigit(ch) {
			return
		}
	}

	order.CurState = fsm.CONFIRMING

	confirmQuery := "Confirm? [Y/N]"
	botMsg := tgbotapi.NewMessage(msg.Chat.ID, confirmQuery)
	botMsg.ReplyToMessageID = msg.MessageID

	_, err := bot.botAPI.Send(botMsg)
	if err != nil {
		log.Printf("Ошибка при отправке сообщения: %v", err)
	}

	order.Cost = msg.Text
}

func (bot *Bot) HandleNameMessage(order *fsm.UserOrder, msg tgbotapi.Message) {
	if len(msg.Text) == 0 {
		return
	}

	for _, ch := range msg.Text {
		if !unicode.IsLetter(ch) && !unicode.IsDigit(ch) {
			return
		}

		if unicode.IsLetter(ch) {
			order.CurState = fsm.WAITING_AMOUNT
		}
	}

	if order.CurState != fsm.WAITING_AMOUNT {
		return
	}

	amountQuery := "Enter the amount"
	botMsg := tgbotapi.NewMessage(msg.Chat.ID, amountQuery)
	botMsg.ReplyToMessageID = msg.MessageID

	_, err := bot.botAPI.Send(botMsg)
	if err != nil {
		log.Printf("Ошибка при отправке сообщения: %v", err)
	}

	order.GoodName = msg.Text
}
