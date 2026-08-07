---
title: "If your submitters say your email never arrived"
section: "05-emails"
audience: organisers
plan: all plans (including free Basic)
last_reviewed: 2026-07-29
---

# If your submitters say your email never arrived

## Work down this list in order — the sent log answers most cases in a few seconds, and tells you whether the problem is at your end or theirs.

This guide is for event administrators. 

**Start with the sent log: Event dashboard → Emails → Sent logs.**

If the email is **not listed there, it never sent.** Nothing further to diagnose — go
back and send it again. This is the single most useful check, and it separates "did
not send" from "sent but did not arrive", which have completely different causes.

## The email is in the log but they still say it did not arrive

**Check for a bounce.** In the sent log, use **Show bounced messages** in the top
right. A bounce tells you the message reached their mail server and was refused.

Common reasons, in the order they actually happen:

* **It went to spam.** Much the most common, especially with university addresses
  and especially for verification emails. Ask them to check their spam or junk
  folder, and to ask their IT department to allow mail from Oxford Abstracts. Some
  institutions filter aggressively enough that nothing gets through.
* **Their mailbox is full.** A mailbox that is over quota refuses new mail. They will
  need to clear space, or give you a different address.
* **Their mail provider is blocking us.** Occasionally a recipient's provider blocks
  our sending address outright. Nothing at your end will fix this — see below.

## If one specific person never receives anything

An address that has **hard bounced** in the past is suppressed automatically, and
will not receive anything from Oxford Abstracts from then on — including from a
different event, and sometimes years later. This is why one person can be the only
one missing every email you send.

You cannot clear this yourself. [Contact support](https://oxfordabstracts.com/resources/contact-support/)
with the address and ask for it to be released, and it can be unblocked the same
day. If it hard bounces again afterwards, the problem is at their end and they will
need to use a different address.

## Before you assume it is your setup

If several people report missing emails at once and nothing appears in the sent log
at all, check whether it is affecting your whole event rather than one recipient.
Occasional platform-wide email incidents do happen and are resolved quickly — any
email that does not appear in the log has not gone out, so simply send it again once
things are working.

## Reduce it happening in the first place

Sending from your own address needs DKIM validation, or mail is more likely to be
filtered. See [Why does my email need to be DKIM validated?](/05-emails/why-does-my-email-need-to-be-dkim-validated.html)
and [What domains will emails from Oxford Abstracts originate from?](/05-emails/what-domains-will-emails-from-oxford-abstracts-originate-from.html)
so you can tell people what to allow.
