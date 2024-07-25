import requests
from requests.auth import HTTPBasicAuth

baseUrl = "http://pms1.hotelstask.com:18686"
class hotelAPI():
    def __init__(
            self, 
            getURL={
                "hotelData": f"{baseUrl}/api/hotel/info",
                "availableRooms": f"{baseUrl}/api/room/availability",
                "travelAgents": f"{baseUrl}/api/travel/agent"
            },
            postURL={
                "createBooking": f"{baseUrl}/api/booking/create",
                "checkBookingPrice": f"{baseUrl}/api/booking/price"
            },
            username: str = "admin",
            password: str = "admin"
        ):
        """
        Constructor of hotel API
        :param getURL: A dictionary containing all GET APIs
        :param postURL: A dictionary containing all POST APIs
        :param username: Username for API authentication
        :param password: Password for API authentication
        """
        self.getURL = getURL
        self.postURL = postURL
        self.basicAuth = HTTPBasicAuth(username=username, password=password)

    def getHotelData(self):
        """
        A method that returns hotel data such as name, room types, rate plans, etc...
        :return Dictionary of hotel Data
        """
        self.getResponse = requests.get(self.getURL["hotelData"], auth=self.basicAuth)
        self.data = self.getResponse.json()["response"]
        return self.data["hotels"][0]
    
    def getTravelAgents(self):
        """
        A method that returns travel agents
        :return Dictionary of travel agents
        """
        self.getResponse = requests.get(self.getURL["travelAgents"], auth=self.basicAuth)
        self.data = self.getResponse.json()["response"]

        return self.data
    
    def getRoomsAvailable(self, checkInDate, checkOutDate):
        """
        A method that returns number and type of available rooms between given check in and check out dates.
        :param checkInDate: format "YYYY-mm-dd"
        :param checkOutDate: format "YYYY-mm-dd"
        :retrun Dictionary of available rooms and their data
        """
        headers = {
            "check_in": checkInDate,
            "check_out": checkOutDate,
            "hotel": "1"
        }
        self.getResponse = requests.get(self.getURL['availableRooms'], headers=headers,auth=self.basicAuth)
        self.data = self.getResponse.json()["response"]
        for i in self.data["room_availability"]:
            i["rate_types"] = i["rate_plans"]
            del i["rate_plans"]
        return self.data
        
    def postCreateBooking(self, postData):
        """
        A method that posts booking data to be saved to API.
        :param postData: a dictionary with keys 'hotel_id', 'check_in', 'check_out', 'guest_name', 'mobile', 'group_booking'=True/False, 'lines'=[{'room_type_id','rate_type_id','number_of_rooms'}, {'room_type_id','rate_type_id','number_of_rooms'}, ...]
        :return booking ID
        """
        self.postResponse = requests.post(self.postURL["createBooking"],json=postData, auth=self.basicAuth)
        if (self.postResponse.status_code == 200):
            self.postResponse = self.postResponse.json()
            return self.postResponse["result"]["response"]["booking_number"]
        else:
            print(self.postResponse.status_code)
            print(self.postResponse.reason)
            print("\n\n", self.postResponse)

    def postBookingPrice(self, postData):
        """
        A method that returns the price of desired booking info.
        :param postData: a dictionary with keys 'hotel_id', 'check_in', 'check_out', 'lines'=[{'room_type_id','rate_type_id','number_of_rooms'}, {'room_type_id','rate_type_id','number_of_rooms'}, ...]
        :retrun Total price
        """
        self.postResponse = requests.post(self.postURL["checkBookingPrice"],json=postData, auth=self.basicAuth)
        if (self.postResponse.status_code == 200):
            self.postResponse = self.postResponse.json()
            return self.postResponse["result"]["response"]["total_price"]
        else:
            print(self.postResponse.status_code)
            print(self.postResponse.reason)
            print("\n\n", self.postResponse)