# My Out of SES Sandbox Request

## Describe how you will comply with AWS Service Terms and AUP - optional

All emails will be sent while mindful of the AWS Service Terms and AUP. There will be no email or message abuse, as all emails sent will be specifically requested by each user.

## Describe how you will only send to recipients who have specifically requested your mail - optional

There are only two circumstances in which our application will send email.
(A) A user requests an email in order to perform a password reset.
(B) A user requests an email in order to verify that they own the email address they used to sign up for the website.
In both cases the user must specifically request the email be sent.

## Describe the process that you will follow when you receive bounce and complaint notifications - optional

On any bounce or complaint notification the target address will be added to blacklist within the application, and thus no longer receive email from the site.

## Use case description

We plan to use SES to send emails to users of lewdix.com.
There is no mailing list for our application.
Emails that result in bounces and/or complaints will be blacklisted, and the application will no longer send to those addresses.
All emails must be individually requested. Thus, there is no need for a user to opt out.
This is a hobbyist project. Thus, we decided to keep the default sending rate and quota to start.
