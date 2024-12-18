<div id="top" align="center">
	  <img src="https://github.com/user-attachments/assets/88780687-0ffb-4166-9b3d-df6b6b3e73cc" height="150"  />

 <div id="badges">

  </div>
	<br/><br/>
  <a href="https://github.com/ahlem-phantom/django-travel-agency/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/ahlem-phantom/django-travel-agency.svg?style=for-the-badge"/>
  </a>

  <a href="https://github.com/ahlem-phantom/django-travel-agency/issues">
    <img src="https://img.shields.io/github/issues/ahlem-phantom/django-travel-agency.svg?style=for-the-badge"/>
  </a>

  <a href="https://github.com/ahlem-phantom/django-travel-agency/stargazers">
    <img src="https://img.shields.io/github/stars/ahlem-phantom/django-travel-agency.svg?style=for-the-badge"/>
  </a>
   <a href="https://github.com/ahlem-phantom/django-travel-agency/network/members">
      <img src="https://img.shields.io/github/forks/ahlem-phantom/django-travel-agency.svg?style=for-the-badge"/>
    </a>
<h3 align="center">Django Travel Agency</h3>
  
  <p align="center">
This is the official Django Travel Agency documentation <br/><br/>
    <img src="https://github.com/user-attachments/assets/030aa45d-1d69-4bc4-abe1-6c90139f5e62"  height="300"/>

  </p>
 </div>
 

### 📐 Project Description 
This project involves developing a web application for a travel agency using Django. The app will provide users with the ability to browse, book, and pay for various travel packages. Additionally, the application will send email confirmations, generate PDF invoices, and offer customer support through an integrated chatbot.
Key features of the application include:
1. **User Booking & Payment:** Users can browse different travel packages, view details, and book their trips through the platform. Payment integration will allow users to pay securely for their bookings.
2. **Email Confirmation:** Upon completing a booking, the system will asynchronously send an email confirmation to the user, leveraging Celery with RabbitMQ as the message broker.
3. **PDF Invoice Generation:** After booking, the system will generate and send a PDF invoice to the user’s email. This will be done using WeasyPrint library to dynamically generate invoices based on booking details.
4. **Travel News Scraping:** The app will scrape travel news websites using BeautifulSoup tool to gather the latest news and tips. These articles will be stored in the app’s database for easy access by users.
5. **Personalized Recommendations:** The system will analyze user preferences and feedback, and provide personalized recommendations for packages, activities, or destinations using libraries such as NumPy or SciPy for calculations.
<p align="right">(<a href="#top">back to top</a>)</p>

### 🚀 Built With

**This project** was built using Django. You may find below the list of the frameworks/libraries that I used to build this project :
<br/>
1. **Django** (Web Framework)
2. **Celery** (Asynchronous Task Management)
3. **RabbitMQ** (Message Broker)
4. **SQLite** (Database)
5. **BeautifulSoup** (Web Scraping)
6. **WeasyPrint** (PDF Generation)
7. **NumPy** (Data Processing)

 
  
<p align="right">(<a href="#top">back to top</a>)</p>


## ✨ Getting Started
To get a local copy up and running follow these simple example steps.

### 🚧 Prerequisites

You may find below the list of things you need to use this project :
* Python installed on your system.
* RabbitMQ installed and running.
* GTK3 installed to enable WeasyPrint to work properly (for generating PDF files).

### 🛠 Installation

_In order to install the app you need to follow the instructions below :_
1. Clone the repo
   ```sh
   git clone https://github.com/ahlem-phantom/django-travel-agency.git
   ```


 #### Project backend :
2. Create a virtual environement and activate it 
   ```sh
   ($) python3 -m venv venv
   ($) .\venv\Scripts\activate.bat
   ```  
3. Install flask dependecies using the file "requirements.txt"
   ```sh
   pip install -r requirements.txt
   ```
4. Rename the file .env_template and fill it with your flouci api credentials with your email settings 
```sh
  FLOUCI_APP_TOKEN=your-app-token-here
  FLOUCI_APP_SECRET=your-app-secret-here
  EMAIL_HOST_USER = 'your-mail-address-here'
  EMAIL_HOST_PASSWORD = 'your-mail-password-her'
  DEFAULT_FROM_EMAIL = 'your-mail-address-here'
   ```
5. Run Django Migrations 
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py migrate django_celery_results
   ```


6. Create a Superuser Account for Admin Access
   ```sh
   python manage.py createsuperuser
   ```
You'll be prompted to enter a username, email, and password for the admin account. After the superuser is created, you'll be able to log in to the Django admin dashboard.

7. Run the django server
   ```sh
   python manage.py runserver
   ```

8. Open localhost:8000 to enjoy the app.

   
#### Celery Setup :

9. Start RabbitMQ (ensure RabbitMQ is installed and running)
   ```sh
   rabbitmq-server 
   ```
10. Enable RabbitMQ Management Plugin:
  ```sh
  rabbitmq-plugins enable rabbitmq_management
  ```
This will enable the web interface at http://localhost:15672. You can log in using the default credentials (guest as both the username and password).

11. Start the Celery worker
   ```sh
   celery -A django_travel_agency worker --loglevel=info
   ```


| <img src="https://github.com/user-attachments/assets/25328ccc-3aed-4f6f-b0b6-92529c4e8b38"/>  <br>**Storage of Celery Task Results in the database**| <img src="https://github.com/user-attachments/assets/5a5a369c-7867-4fda-863a-1805f7ab1d15" />  <br>**RabbitMQ**| 
| ------------- |------------- | 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## ⚡ Usage

- **Browse Packages**: Navigate to the homepage to view all available travel packages.
- **Book a Trip**: Select a package, provide your details, and complete the payment process.
- **Receive Confirmation**: Check your email for the booking confirmation and attached PDF invoice.
- **Get Recommendations**: Get top rated travel recommendations.


Start by exploring the available travel packages and choose the one that suits your preferences.
| <img src="https://github.com/user-attachments/assets/b6121784-5cc8-4133-a60a-332bfb980837" width="900" height="600"/><br> **Browse Packages**| 
| ------------- |

Proceed to the booking form where you can:
1. Select the number of adults and children.
2. Enjoy dynamic pricing: Children receive a 50% discount, and the total price updates in real-time based on your selection.
3. Choose your preferred payment method: Pay online or on-site for added flexibility.

| <img src="https://github.com/user-attachments/assets/ed04935c-850d-487f-870d-0f9b8b10ea1e" width="900" height="600"/>  <br>**Book a Trip**| 
| ------------- |

Once the online payment is picked, a payment URL will be generated, redirecting you to the payment page. To simulate a successful transaction, enter "111111" and you will be redirected to the success page. For a failed payment, use "0000000" to be redirected to the failure page.
| <img src="https://github.com/user-attachments/assets/198604f7-1a4c-45c2-8feb-779141ff0c79" /><br> **Flouci Payment**| <img src="https://github.com/user-attachments/assets/499e1a71-a64e-42f4-9ac4-3de960686cd7" />  <br>**Booking Success**| 
| ------------- | ------------- | 

Upon Booking a pdf invoice will be generated asynchronysly and you will recieve a confirmation mail:
| <img src="https://github.com/user-attachments/assets/493d7e4a-fdd1-4590-8520-c4dcdc644a0a" /><br> **PDF INVOICE**| <img src="https://github.com/user-attachments/assets/c7087302-a1e1-44f6-bc51-039be12908a9" />  <br>**Booking Confirmation Email**| 
| ------------- | ------------- | 


You can also explore the latest travel news, trends, and expert tips, all conveniently gathered through web scraping. 
| <img src="https://github.com/user-attachments/assets/eb243426-8b6d-4d6f-ae16-71f67e2bbd14"/>  <br>**News Articles Scraping**| <img src="https://github.com/user-attachments/assets/c3c9c2ff-2ec8-42f4-be8d-6f0846335ff2" />  <br>**News Articles Source: https://www.lonelyplanet.com/news**| 
| ------------- |------------- | 


I started this but didn't have time to finish it all. I created an assistant to guide users through the booking process and gather user feedback, but time was short. I also built a recommendation system, but it's not strong enough as it relies on ratings that I personally added to the database for each travel package and user gender. It lacks user data like feedback and preferences.
| <img src="https://github.com/user-attachments/assets/07c2f23c-de2e-4633-878e-3673844ec4fd"/>  <br>**Chatbot Assistant**| <img src="https://github.com/user-attachments/assets/976c0402-03df-486c-a097-6dbdedeed901" />  <br>**Packages Recommandations**| 
| ------------- |------------- | 


<!-- CONTACT -->
## 💌 Contact

<b>Project Author :</b> 
| <img src="https://user-images.githubusercontent.com/78981558/157719496-9aec4730-512f-4188-87ca-8dbe6271ebfc.jpg" width="150" height="150"/>  <br> **Ahlem Laajili**| 
| ------------- |
|<div align="center"><a href="mailto:ahlem.laajili@esprit.tn"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail Badge"/></a><a href="https://github.com/ahlem-phantom"><img title="Follow on GitHub" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/></a></div>  |


<p align="right">(<a href="#top">back to top</a>)</p>




Developed with 💕 by **ahlem-phantom**.
