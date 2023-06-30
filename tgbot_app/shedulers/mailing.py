# async def schedule_mailing():
#     mails = await get_adv()
#
#     if not mails['paid'] + mails['unpaid'] + mails['all']:
#         return
#
#     subscribed_users = await get_users_id(subscribed=True)
#     unsubscribed_users = await get_users_id(subscribed=False)
#     all_users = subscribed_users + unsubscribed_users
#
#     if mails['paid']:
#         for mail in mails['paid']:
#             await send_mail(mail, subscribed_users)
#
#     if mails['unpaid']:
#         for mail in mails['unpaid']:
#             await send_mail(mail, unsubscribed_users)
#
#     if mails['all']:
#         for mail in mails['all']:
#             await send_mail(mail, all_users)