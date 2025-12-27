package main

import (
	"mybot/bot"
)


func main() {
	var myBotToken string = "8211768908:AAFqZ4zmcI-W6BsKjFKpNC3rTAOM3emzvK4"
	var myBot bot.Bot
	myBot.Init(myBotToken)
	myBot.SetUpdate(0, 60)
	myBot.StartListen()
	myBot.ProcessOrders()
}
