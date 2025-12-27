package fsm

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type State int

const (
	WAITING_NAME State = iota
	WAITING_AMOUNT
	CONFIRMING
	SUCCESS
)

type UserOrder struct {
	GoodName  string
	Cost      string
	IsConfirm bool
	CurState  State
}

type MessageHandlers func(order *UserOrder, msg tgbotapi.Message)
