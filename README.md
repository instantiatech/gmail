# PythonからGmailを送信

## 使い方

```python
import gmail

USER_ADDRESS = "foo@gmail.com"
USER_PASSWORD = "hogehoge"

gmail_obj = gmail.Gmail(USER_ADDRESS, USER_PASSWORD)

FROM_ADDRESS = "foo@gmail.com"
TO_ADDRESS = "bar@gmail.com"
SUBJECT = "test subject"
body = "test body"

gmail_obj.send(FROM_ADDRESS, TO_ADDRESS, SUBJECT, body)
```
