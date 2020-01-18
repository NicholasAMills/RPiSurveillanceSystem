'''
    Class to hold username and password for email, along with recpient email as a QOL improvement.

    NOTE: get_username() email MUST be a gmail account. get_recipient() can be any email address.
    Basic idea is to send it to yourself. If you don't use gmail as your primary email, create one just for this sole
    purpose and then make the recipient your primary email address. This is where you receive the photos from as
    attachments.
'''

class Login():
    def get_username():
        return 'your gmail here' # enter a gmail account here inside the single quotes. This must be a gmail account.

    def get_password():
        return 'your email password here' # enter your gmail password here inside the single quotes

    def get_recipient():
        return 'recipient email here' # enter destination email inside the single quotes
