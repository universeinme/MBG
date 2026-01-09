# def kirim_email(perusahaan,subject,body,path_surat,path_cv):
#     return str(perusahaan,subject,body,path_surat,path_cv)

import os
import yagmail

def kirim_email(
    to_email,
    subject,
    body,
    path_surat,
    path_cv
    # dry_run=True
):
    try:
        # --- normalize ---
        attachments = []

        if path_surat:
            attachments.append(path_surat)

        if path_cv:
            attachments.append(path_cv)

        # --- validation ---
        if not to_email:
            return "FAILED: to_email kosong"
        if not subject:
            return "FAILED: subject kosong"
        if not body:
            return "FAILED: body kosong"

        # --- dry run ---
        # if dry_run:
        #     return "DRY_RUN"

        # --- credentials ---
        user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_APP_PASSWORD")

        if not user or not password:
            return "FAILED: email credential tidak ditemukan"

        # --- init yagmail ---
        yag = yagmail.SMTP(user=user, password=password)
        # yag = yagmail.SMTP()

        # --- send ---
        yag.send(
            to=to_email,
            subject=subject,
            contents=body,
            attachments=attachments
        )

        return "Email Terkirim"

    except Exception as e:
        return f"FAILED: {str(e)}"
