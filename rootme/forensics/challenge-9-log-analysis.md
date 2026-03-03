# Analyse de logs - Attaque web

#### Énoncé

Notre site web semble avoir été attaqué, mais notre administrateur système ne comprend pas les logs du serveur web. Pouvez-vous retrouver les données qui ont été exfiltrées ?

Enormous txt file with HTTP requests.

Looking more or less like this.

	192.168.1.23 - - [18/Jun/2015:12:12:54 +0200] "GET /admin/?action=membres&order=QVNDLChzZWxlY3QgKGNhc2UgZmllbGQoY29uY2F0KHN1YnN0cmluZyhiaW4oYXNjaWkoc3Vic3RyaW5nKHBhc3N3b3JkLDEsMSkpKSwxLDEpLHN1YnN0cmluZyhiaW4oYXNjaWkoc3Vic3RyaW5nKHBhc3N3b3JkLDEsMSkpKSwyLDEpKSxjb25jYXQoY2hhcig0OCksY2hhcig0OCkpLGNvbmNhdChjaGFyKDQ4KSxjaGFyKDQ5KSksY29uY2F0KGNoYXIoNDkpLGNoYXIoNDgpKSxjb25jYXQoY2hhcig0OSksY2hhcig0OSkpKXdoZW4gMSB0aGVuIFRSVUUgd2hlbiAyIHRoZW4gc2xlZXAoMikgd2hlbiAzIHRoZW4gc2xlZXAoNCkgd2hlbiA0IHRoZW4gc2xlZXAoNikgZW5kKSBmcm9tIG1lbWJyZXMgd2hlcmUgaWQ9MSk%3D HTTP/1.1" 200 1005 "-" "-"

We have a base64 encoded parameter in the "order". When looking in the log, we have two different functions being sent

Here the attacker will be comparing every ASCII bit of every character composing the password of the member=1 (supposedly the first member created in the database, admin)
Without returning the password directly by the sql, the attacker is comparing like i said every bit with 00, 01, 10, or 11.
In SQL.

So we have in the logs a repetition of 3 functions, each one comparing a pair of bits, so, (12), (34), (56). And then we have a shorter function that only compares the last bit (7).
Comparing bits by pair is a great optimisation to greatly reduce the amount of queries. 

The "longer function" comparing bits by the pair, executed 3 times in a row.
```sql 
ASC,(select (case field(concat(substring(bin(ascii(substring(password,1,1))),1,1),substring(bin(ascii(substring(password,1,1))),2,1)),concat(char(48),char(48)),concat(char(48),char(49)),concat(char(49),char(48)),concat(char(49),char(49)))when 1 then TRUE when 2 then sleep(2) when 3 then sleep(4) when 4 then sleep(6) end) from membres where id=1)

```

"Shorter" function comparing only the last ASCII bit (7) executed the 4th time, last one of a "block"
```sql
ASC,(select (case field(concat(substring(bin(ascii(substring(password,1,1))),7,1)),char(48),char(49)) when 1 then sleep(2) when 2 then sleep(4)  end) from membres where id=1)
```

The attacker will return a sleep(x), with x being a certain amount of distinguishable time, if the value of the ASCII binary is equal to a certain binary value.
In this case, absence of delay corresponds to the first case ,00. if the server sleeps for 2 seconds, the value is 01, if the server sleeps for 4 seconds, the value is 10, and finally 11 if the server sleeps for 6 seconds.
The attacker basically uses response time as a covert communication channel.

In the case of the last bit, the server will sleep for 2 seconds if the value is 0, and 4 seconds if the value is 1. 
There is a specific case when the last bit doesn't return a sleep value and the delay of the request is 0 seconds. In that case, it just means that the value didn't have a matching case in the function, meaning that there is no bit at this position (the character is only encoded on 6 bits, MySQL doesn't pad zeroes).

Considering this, the method here is calculating the time deltas between the request to have a binary chain which we can then convert to ASCII to get the requested data.

The script works like this :

Creating a regex in order to extract the timestamp and the data of every line in the log file

Opening the file, for every line matching the regex :
Append the timestamp to a list, converted to a parsed time object.
decode the payload base64 part to utf8
search the current bit position in the payload part.

For every timestamp, calculate the time delta between the next timestamp and the current one.

For every bit except the 7, add the corresponding binary par value to the current byte string

If its the 7th bit, return 0 or 1 or "" depending on the time delta read.
add the last bit to the current byte string.
pad the byte with 0s to the left to attain 8 characters
add the converted char to the password chain

retrieve the password. 