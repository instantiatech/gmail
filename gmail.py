import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Gmail(object):
    """
    gmail送信クラス
    """

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587

    def __init__(self, user_address, user_password):
        """コンストラクタ

        Args:
            user_address: ユーザのメールアドレス
            user_password: パスワード
        """

        self.user_address = user_address
        self.user_password = user_password

    def send(
        self,
        from_address,
        to_addresses,
        subject,
        body,
        attachments=None,
        profile=None,
        cc_addresses=None,
        bcc_addresses=None,
    ):
        """メールを送信する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            attachments: 添付ファイル
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        """

        if attachments:
            msg = self.create_body_with_attachment(
                from_address, to_addresses, subject, body, attachments, profile, cc_addresses, bcc_addresses
            )
        else:
            msg = self.create_body(from_address, to_addresses, subject, body, profile, cc_addresses, bcc_addresses)

        send_list = self.create_address_list(to_addresses)

        if cc_addresses:
            send_list += self.create_address_list(cc_addresses)

        if bcc_addresses:
            send_list = self.create_address_list(bcc_addresses)

        smtpobj = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()

        smtpobj.login(self.user_address, self.user_password)
        smtpobj.sendmail(from_address, send_list, msg.as_string())
        smtpobj.close()

    def create_body_with_attachment(
        self,
        from_address,
        to_addresses,
        subject,
        body,
        attachments=None,
        profile=None,
        cc_addresses=None,
        bcc_addresses=None,
    ):
        """添付ファイル付きのメール本文を作成する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            attachments: 添付ファイル
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        Returns:
            メール本文
        """

        msg = MIMEMultipart()
        msg = self.create_msg(msg, from_address, to_addresses, subject, profile, cc_addresses, bcc_addresses)
        body = MIMEText(body.encode("utf-8"), "html", "utf-8")
        msg.attach(body)

        if type(attachments) is str:
            attachments = [attachments]

        for attachment in attachments:
            base_name = os.path.basename(attachment)
            with open(attachment, "rb") as f:
                part = MIMEApplication(f.read(), Name=base_name)

            part["Content-Disposition"] = 'attachment; filename="{}"'.format(base_name)
            msg.attach(part)

        return msg

    def create_body(self, from_address, to_addresses, subject, body, profile, cc_addresses=None, bcc_addresses=None):
        """メール本文を作成する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        Returns:
            メール本文
        """

        msg = MIMEText(body.encode("utf-8"), "html", "utf-8")
        return self.create_msg(msg, from_address, to_addresses, subject, profile, cc_addresses, bcc_addresses)

    @staticmethod
    def create_msg(msg, from_address, to_addresses, subject, profile=None, cc_addresses=None, bcc_addresses=None):
        msg["Subject"] = subject
        if profile:
            msg["From"] = "{} <{}>".format(Header(profile.encode("utf-8"), "utf-8").encode(), from_address)
        else:
            msg["From"] = from_address

        def to_string_addresses(addresses):
            if type(addresses) is str:
                return addresses
            elif hasattr(addresses, "__iter__"):
                return ",".join(addresses)

        msg["To"] = to_string_addresses(to_addresses)

        if cc_addresses:
            msg["Cc"] = to_string_addresses(cc_addresses)

        if bcc_addresses:
            msg["Bcc"] = to_string_addresses(bcc_addresses)

        msg["Date"] = formatdate()

        return msg

    @staticmethod
    def create_address_list(addresses):
        if type(addresses) is str:
            send_list = [addresses]

        elif hasattr(addresses, "__iter__"):
            send_list = [address for address in addresses]
        else:
            raise Exception("argument has to be str or iterable")

        return send_list
