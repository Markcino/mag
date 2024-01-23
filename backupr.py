#!/usr/bin/env python3
import os
import shutil
import fnmatch
from tqdm import tqdm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

src_file = 'C:/Users/Mark.Gbalazeh/Desktop/Test/mbsdbs'
des_path = 'C:/Users/Mark.Gbalazeh/Desktop/Test/b'

chunk_size = 1024 * 1024 

recipients = ["markcinogbalazeh@gmail.com"]

def send_success_email():
    subject = "Copying Finished: TEST EMAIL"
    message = "Copying has been completed successfully!"

    msg = MIMEMultipart()
    msg['From'] = "cabetech25@gmail.com"
    msg['To'] = ", ".join(recipients) 
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("cabetech25@gmail.com", "jstlinjogqgbsqlr")
    text = msg.as_string()
    server.sendmail("cabetech25@gmail.com", recipients, text)
    server.quit()


def send_error_email(error_message):
    subject = "TEST EMAIL: FAIL TO COPY"
    message = f"Please disregard this email, it is a test mail: Failed to Copy Filed, Please Retry Again. Error: {error_message}"

    msg = MIMEMultipart()
    msg['From'] = "cabetech25@gmail.com"
    msg['To'] = ", ".join(recipients) 
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("cabetech25@gmail.com", "jstlinjogqgbsqlr")
    text = msg.as_string()
    server.sendmail("cabetech25@gmail.com", recipients, text)
    server.quit()


def copy_files(ftype, prefix=""):
    try:
        directories = [dir for dir in os.listdir(src_file) if os.path.isdir(os.path.join(src_file, dir))]

        if not directories:
            raise ValueError("No Most Recent Folder Created, Please Wait!! or Refresh")

        most_recent_dir = max(directories, key=lambda dir: os.path.getctime(os.path.join(src_file, dir)))

        source = os.listdir(os.path.join(src_file, most_recent_dir))
        source = [file for file in source if fnmatch.fnmatch(file, ftype)]

        if not source:
            raise ValueError("No Most Recent File Created, Please Wait!! or Refresh")

        source.sort(key=lambda file: os.path.getctime(os.path.join(src_file, most_recent_dir, file)), reverse=True)

        for most_recent_file in source:
            full_file_name = os.path.join(src_file, most_recent_dir, most_recent_file)

            now = datetime.now()

            folder_name = now.strftime("%Y%m%d")

            new_folder_path = os.path.join(des_path, prefix + folder_name + "_DAT")

            if os.path.exists(new_folder_path):
                shutil.rmtree(new_folder_path)

            os.mkdir(new_folder_path)

            total_size = os.path.getsize(full_file_name)
            copied_size = 0

            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Copying files", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as progress_bar:
                with open(full_file_name, 'rb') as source_file: 
                    with open(os.path.join(new_folder_path, os.path.basename(full_file_name)), 'wb') as dst_file:
                        while True:
                            chunk = source_file.read(chunk_size)  
                            if not chunk:
                                break
                            dst_file.write(chunk)
                            copied_size += len(chunk)
                            progress_bar.update(len(chunk))
            send_success_email()

    except Exception as e:
        send_error_email(str(e))

copy_files("*.BAK")
copy_files("*IMAGEN", "IMAGEN")