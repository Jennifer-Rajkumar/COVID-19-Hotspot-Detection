import folium
# importing the required libraries
import pandas as pd

# Visualisation libraries
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine


# Manipulating the default plot size
plt.rcParams['figure.figsize'] = 10, 12

# Disable warnings 
import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

app=Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'vaccine',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

states=[]
content=[]
image=[]
d={}
st=""
dis=""
hosp=[]
find=""

f={'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Vishakhapatnam', 'Vizianagaram', 'West Godavari', 'YSR Kadapa'], 
   'Arunachal Pradesh': ['Papum Pare'], 
   'Assam': ['Nagaon', 'Dibrugarh', 'Sivasagar', 'Kamrup Metro', 'Goalpara', 'Barpeta', 'Kamrup', 'Lakhimpur', 'Dhemaji', 'Sonitpur', 'Jorhat', 'Biswanath', 'Cachar', 'Karbi Anglong', 'Darrang', 'Golaghat', 'Tinsukia', 'Hojai', 'Dima Hasao', 'Bongaigaon', 'Kokrajhar', 'Karimganj', 'Nalbari', 'Hailakandi', 'Marigaon'], 
   'Bihar': ['Aurangabad', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Darbhanga', 'Gaya', 'Gopalganj', 'Jamui', 'Katihar', 'Khagaria', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Pashchim Champaran', 'Patna', 'Purbi Champaran', 'Purnia', 'Rohtas', 'Samastipur', 'Saran', 'Sitamarhi', 'Siwan', 'Vaishali', 'Araria', 'Saharsa'], 
   'Chandigarh': ['Chandigarh'], 
   'Chhattisgarh': ['Baloda Bazar', 'Raipur', 'Bilaspur', 'Kanker', 'Dhamtari', 'Balod', 'Bastar', 'Bemetara', 'Durg', 'Gariyaband', 'Janjgir-Champa', 'Jashpur', 'Kabirdham', 'Kondagaon', 'Korba', 'Korea', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Rajnandgaon', 'Sukma', 'Surguja'], 
   'Jharkhand': ['Deoghar', 'Dhanbad', 'Pakur', 'Bokaro', 'Garhwa', 'Jamtara', 'Lohardaga', 'Ranchi', 'Saraikela Kharsawan', 'Chatra', 'Dumka', 'East Singhbum', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Khunti', 'Koderma', 'Latehar', 'Palamu', 'Ramgarh', 'Sahebganj', 'Simdega', 'West Singhbhum'], 
   'Delhi': ['Central', 'East', 'New delhi', 'North', 'North West', 'South', 'South East', 'South West', 'West'], 
   'Goa': ['North Goa', 'South Goa'], 
   'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Arvalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhotaudepur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kachchh', 'Kheda', 'Mahesana', 'Morbi', 'Mahisagar', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabar Kantha', 'Surat', 'Surendranagar', 'Sabarkantha', 'Tapi', 'Vadodara', 'Valsad'], 
   'Haryana': ['Ambala', 'Bhiwani', 'Charki Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Mewat', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamuna Nagar'], 
   'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Mandi', 'Sirmaur', 'Solan', 'Una'], 
   'Jammu and kashmir': ['Kupwara', 'Kulgam', 'Pulwama', 'Srinagar', 'Anantnag', 'Badgam', 'Jammu', 'Kathua', 'Reasi', 'Samba', 'Udhampur'], 
   'Karnataka': ['Bagalkote', 'Ballari', 'Belagavi', 'Bengaluru', 'Bengaluru Rural', 'Bidar', 'Chamarajanagara', 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura'], 
   'Kerala': ['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'], 
   'Madhya Pradesh': ['Anuppur', 'Balaghat', 'Barwani', 'Betul', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Vidisha'], 
   'Maharashtra': ['Ahmadnagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondiya', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai & Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal'], 
   'Manipur': ['Churachandpur', 'Imphal East', 'Imphal West', 'Kakching'], 
   'Meghalaya': ['East Khasi Hills', 'Ri Bhoi', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'], 
   'Mizoram': ['Aizawl', 'Champhai'], 
   'Nagaland': ['Dimapur', 'Kohima', 'Mokokchung', 'Tuensang'], 
   'Puducherry': ['Pondicherry'], 
   'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Firozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Pathankot', 'Patiala', 'Rupnagar', 'S.A.S Nagar', 'Sangrur', 'Shahid Bhagat Singh Nagar', 'Sri Muktsar Sahib', 'Tarn Taran'], 
   'Sikkim': ['East District'], 
   'Tamil Nadu': ['Ariyalur', 'Chennai', 'Cuddalore', 'Coimbatore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kanyakumari', 'Kallakurichi', 'Kancheepuram', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Namakkal', 'Nagapattinam', 'Nilgiris', 'Pudukottai', 'Perambalur', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivagangai', 'Thanjavur', 'Tirunelveli', 'Tiruvannamalai', 'Tuticorin', 'Theni', 'Thirupathur', 'Thiruvallur', 'Tiruchirappalli', 'Tirupur', 'Tiruvallur', 'Tiruvarur', 'Vellore', 'Villupuram', 'Virudunagar'], 
   'Telangana': ['Hyderabad', 'Medchal Malkajgiri', 'Ranga Reddy', 'Warangal Urban'], 
   'Tripura': ['West'], 
   'Uttar Pradesh': ['Agra', 'Aligarh', 'Allahabad', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Deoria', 'Etah', 'Etawah', 'Faizabad', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kheri', 'Kushi Nagar', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Rae Bareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabeer Nagar', 'Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharth Nagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'], 
   'Uttarakhand': ['Almora', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Tehri Garhwal', 'Udam Singh Nagar'], 
   'West Bengal': ['24 Paraganas North', 'Howrah', 'Jalpaiguri', 'Kolkata']}

class hospital(db.Document):
    state=db.StringField()
    district=db.StringField()
    details=db.ListField()
    
@app.route("/")
def home():
    my_url = "https://news.google.com/covid19/map?hl=en-IN&mid=%2Fm%2F03rk0&gl=IN&ceid=IN%3Aen"
    
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    
    containers = page_soup.findAll("tbody", {"class": "ppcUXd"})
    container = containers[0]
    
    states = container.findAll("div",{"class":"pcAJd"})
    total_case = container.findAll("td",{"class":"l3HOY"})
    
    states=[states[i].text for i in range(0,len(states))]
    total_case = [total_case[i].text for i in range(0,len(total_case))]
    
    total_case = [total_case[i] for i in range(0,len(total_case),5)]
    total_case = [total_case[i].split(',') for i in range(0,len(total_case))]
    total_case = [int("".join(map(str,total_case[i]))) for i in range(0,len(total_case))]
    
    India_coord = pd.read_excel('Indian Coordinates.xlsx')
    lat = list(India_coord['Latitude'])
    long = list(India_coord['Longitude'])
    st = list(India_coord['Name of State / UT'])
    d = {st[i]:[lat[i],long[i]] for i in range(0,len(st))}
    
    del states[0]
    del states[0]
    
    del total_case[0]
    del total_case[0]
    myMap = folium.Map(location=[20, 70], zoom_start=4,tiles='Stamenterrain')
    for i in range(0,len(states)):
        folium.CircleMarker(d[states[i]], popup = ('<strong>State</strong>: ' + states[i] + '<br>''<strong>Total Cases</strong>: ' + str(total_case[i]) + '<br>'),color='red',fill_color='red' ).add_to(myMap)
    
    # Generate map
    myMap.save('templates/map.html')
    return render_template("home.html")
@app.route("/option")
def option():
    return render_template("option.html")
@app.route("/content")
def content():
    return render_template("content.html")
@app.route("/map")
def myMap():
    return render_template("map.html")
@app.route("/restriction")
def restriction():
    global state,content,image
    my_url = "https://www.goibibo.com/info/statewise-covid-guidelines/"

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    
    containers = page_soup.findAll("p", {"class": "state-head pad-t-6"})
    states=[containers[i].text for i in range(0,len(containers))]
    
    containers = page_soup.findAll("p", {"class": "state-sub-txt"})
    content = [containers[i].text for i in range(0,len(containers))]
    
    containers = page_soup.findAll("div", {"class": "state-img"})
    image = [containers[i].img["src"] for i in range(0,len(containers))] 
    
    for i in range(0,len(states)):
        d[states[i]]=[content[i],image[i]]
    
    return render_template("restriction.html",info=d)

@app.route("/centre")
def centre():
    return render_template("vaccine.html",states=f)

@app.route("/temp",methods=['POST'])
def temp():
    find=request.form['state']
    return render_template("vaccine.html",sample=f[find])
    
@app.route("/vaccine",methods=['POST'])
def vaccine():
    global hosp,dis
    dis=request.form['district'].lower()
    for obj in hospital.objects(district=dis):
        hosp=obj.details   
    return render_template("vaccine.html",info=hosp)
    
if __name__ == '__main__':
    app.run()