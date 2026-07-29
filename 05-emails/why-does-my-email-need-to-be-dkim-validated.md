---
title: "Why does my email need to be DKIM validated?"
section: "05-emails"
audience: organisers
plan: all plans (including free Basic)
source_url: https://help.oxfordabstracts.com/knowledge/why-does-my-email-need-to-be-dkim-validated
last_reviewed: 2026-07-28
---

# Why does my email need to be DKIM validated?

## Understand what DKIM is, how to get DKIM validated and how it affects your Oxford Abstract event.

**Please note:** this Knowledge Base article is for Admins ONLY

  

Google & Yahoo have implemented that all email senders must be DKIM validated.

This is to help protect recipients from receiving malicious emails and to help prevent your emails from being rejected or marked as spam.

**If the email address you use for your Oxford Abstract event is** **not properly DKIM authenticated,** **it could mean that emails sent and received will be considered spam and not reach the intended recipient.**

**What does this mean for you?**Because you are sending emails from your event email address, it's important that your emails don't get marked as spam.

**How to get DKIM validated:**

To do this you will need to be able to:

* Access your admin account Oxford Abstracts
* Access to your DNS (your domain name hosting - e.g. GoDaddy, Namecheap, DreamHost)

If someone else has access to your domain name hosting (IT support team), you can follow the first steps and then email them the instructions for the remaining parts.

**Instructions on how to set up your DKIM authentication:**

1. **Go to your Oxford Abstracts admin dashboard → Emails **> Verify Sender > Copy your DKIM information and return path
2. Go to your Domain Name Settings (in GoDaddy, Namecheap, or whichever provider you use)
3. Add a TXT record for DKIM - paste in the DKIM information from Oxford Abstracts
4. Add a CNAME record for your Return-Path - paste in the information from Oxford Abstracts
5. Note that it can take up to 48 hours for the DNS changes to propagate, so it can be a little while before your domain shows as verified
6. In the meantime, emails will continue to be delivered from no-reply@oxfordabstracts.com with a reply-to address of your sender email

**When should I do this?**

ASAP. Google will begin to reject non-compliant traffic in April.

**What will happen in the meantime until I do this?**

We want to reassure you that we will continue to deliver emails to your users; however if your event email address is not DKIM authenticated, then we will switch the sender email to Oxford Abstract’s default email address: no-reply@oxfordabstracts.com. The Reply-To address will be set to your sender email address, so you will still receive email replies to your email address.

**Need further help?**

We understand this is a technical change and may be tricky.

You can read a more detailed walkthrough [**here**](https://postmarkapp.com/support/article/1046-how-do-i-verify-a-domain) on how to verify your domain but if you’re still stuck, please reach out to the **support desk,** and we are always happy to help.
