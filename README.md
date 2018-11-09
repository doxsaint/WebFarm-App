cloned the peterplanner repo to find that it has certain dependencies

using github:
https://github.com/zombiezen/cardcpx\n
https://github.com/beevik/etree
https://github.com/kennygrant/sanitize
https://github.com/go-sql-driver/mysql

using go:
go get golang.org/x/net
go get -u golang.org/x/text


in peterplanner/main.go:
	Cookie data is somehow extracted and set so that the program can extract information directly from the website.
