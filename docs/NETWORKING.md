# Networking

```text
link web
link net
link check

response = web.get("https://example.com")
write(response.status)
write(response.headers)
write(response.text)

write(net.resolve("example.com"))
write(net.hostname())
write(net.localip())
write(check.port("127.0.0.1", 8080))
```

Use these functions only with systems and services you own or are authorized to test.
