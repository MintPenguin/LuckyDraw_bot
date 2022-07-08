# Lucky_Draw_Bot for discord   

## command
for users
> `##draw [number]` : pick up the number.   
> `##remain` : view remaning numbers.

for manager   
> `##set last [number]` : set the board. (last number: `[number]`, enter one of number 1 to 1024)   
> `##set count [number]` : limit the number of uses. (\~-1: no limit, 0\~: set limit)   
> `##clear count` : reset limit of uses.   
   
   
   
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