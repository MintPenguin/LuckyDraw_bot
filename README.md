# Lucky_Draw_Bot for discord   

## command
for users
> `##draw <number>` : draw the number.   
> `##view board` : view remaining numbers.   

for manager   
> Board   
> `##reset baord <the number of draws>` : Set the board with the number of draws. ( `<the number of draws>`, one of 1 to 1024)   
>    
>  Limit count of draws   
> `##set count <number>` : Set limit the number of draws to `<number>` times. (\~-1: no limit, 0\~: set limit)      
> `##clear count` : Clear draw limit for all users.   
>    
> Change the number of winnings   
> `##add winning <amount> <rank>` : Add `<amount>` winning numbers of the `<rank>`.   
> `##delete winning <amount> <rank>` : delete `<amount>` winning numbers of the `<rank>`.   
   
   
   
## Config Vars
key : value   
(\*: you have to enter it.)   
> \*`LUCKY_DRAW_TOKEN` : token of your bot.   
> `HEROKU_DOMAIN` : your heroku server domain for free tier. make a request every 10 minutes to not sleep. 
>    
> (if you don't have database, do not enter it.)   
> `DB_HOST` : host from your database.   
> `DB_NAME` : database name.   
> `DB_USER` : user name to access your database.   
> `DB_PASS` : password to access your database with `DB_USER` account.   
> `DB_PORT` : port number to access the your database.   