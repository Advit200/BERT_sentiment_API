import boto3
import Config
from botocore.exceptions import ClientError
from datetime import datetime
import numpy as np

client = boto3.client(service_name='ses', region_name=Config.s3_region_name,
                      aws_access_key_id=Config.aws_id, aws_secret_access_key=Config.aws_secret)

# client.verify_email_address(EmailAddress = "aditya.gaurav@kochgs.com")

def create_email_template():
    client.create_template(
        Template = {
            "TemplateName" : "Bitter-Sweet-Success",
            "SubjectPart" : "Trying out SES for bitter sweet.",
            "TextPart" : "This is a trial email from aditya's account.",
            "HtmlPart" : "This is normal text.<b> Text is bold here !!! </b>"
        
        }
    )

    client.create_template(
        Template = {
            "TemplateName" : "Bitter-Sweet-Failure",
            "SubjectPart" : "Trying out SES for bitter sweet.",
            "TextPart" : "CODE FAILED.",
            "HtmlPart" : "</h1> code has failed to run. </h1>"
        
        }
    )

def send_mail(template_name=None,recipient_list=None,source=None):

    try: 
        response = client.send_templated_email(
        Source = source,
        Destination={
            'ToAddresses': recipient_list,
        },
        Template = template_name,
        TemplateData = '{"Trial":"Success-Failure Email"}'
    )
        print("\n\n<<<<<<<<<<   EMAIL HAS BEEN SENT TO THE MENTIONED RECIPIENTS.    >>>>>>>>>>>\n\n")

    except ClientError as e:
        print(e.response['Error']['Message'])

def send_developer_mail(recipient_list=None,source=None,dataset_details=None,df_size=None):

    try: 
        response = client.send_email(
        Source = source,
        Destination={
            'ToAddresses': recipient_list,
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': f'''<h3> Bitter-Sweet scraping details for {datetime.today().strftime("%d-%m-%Y")} </h3>\n\n

                                {dataset_details}\n\n

                                Total size of input file : {df_size}
                                                        
                            '''
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': f'Bitter-Sweet Result for : {datetime.today().strftime("%d-%m-%Y")})',
            },
        }
    )
        print("\n\n<<<<<<<<<<   EMAIL HAS BEEN SENT TO DEVELOPERS.    >>>>>>>>>>>\n\n")

    except ClientError as e:
        print(e.response['Error']['Message'])


if __name__ == "__main__":

    # create_email_template()

    recipient_list = ["karthikeyan.chandrasekar@kochgs.com"]
    source = "aditya.gaurav@kochgs.com"
    send_mail(recipient_list=recipient_list,source=source,template_name="Bitter-Sweet-Success")