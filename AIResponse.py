from system_roles import sys_manage


class AIA():
    def __init__(self, data, agents,api_key= "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", useChatGPT=True):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "getRoomsAvailable",
                    "description": "Get the available rooms between dates taken from the customer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "json_type": {
                                "type": "integer",
                                "description": "Always 0"
                            },
                            "check_in": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                            "check_out": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                        },
                        "required": ["json_type", "check_in", "check_out"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "getBookingPrice",
                    "description": "returns total price after the customer chooses all the rooms needed for booking",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "json_type": {
                                "type": "integer",
                                "description": "Always 1"
                            },
                            "hotel_id": {
                                "type": "integer",
                                "description": "Always 1"
                            },
                            "check_in": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                            "check_out": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                            "lines": {
                                "type": "array",
                                "description": "An array containing data for each room chosen by the customer",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "room_type_id": {
                                            "type": "integer",
                                            "description": "An ID for given room type name",
                                        },
                                        "rate_type_id": {
                                            "type": "integer",
                                            "description": "An ID for given room plan name",
                                        },
                                        "number_of_rooms": {
                                            "type": "integer",
                                            "description": "Number of rooms reserved for this room type",
                                        }
                                    },
                                    "required": ["room_type_id", "rate_type_id", "number_of_rooms"]
                                }
                            }
                        },
                        "required": ["json_type", "hotel_id", "check_in", "check_out", "lines"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "createBooking",
                    "description": "Send json data to create hotel booking",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "json_type": {
                                "type": "integer",
                                "description": "Always 2"
                            },
                            "hotel_id": {
                                "type": "integer",
                                "description": "Always 1"
                            },
                            "guest_name": {
                                "type": "string",
                                "description": "Name of the customer"
                            },
                            "mobile": {
                                "type": "string",
                                "description": "Mobile of the customer"
                            },
                            "group_booking": {
                                "type": "boolean",
                                "description": "Whether this is a group booking or not"
                            },
                            "check_in": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                            "check_out": {
                                "type": "string",
                                "description": "Check in date",
                                "format": "date"
                            },
                            "lines": {
                                "type": "array",
                                "description": "An array containing data for each room chosen by the customer",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "room_type_id": {
                                            "type": "integer",
                                            "description": "An ID for given room type name",
                                        },
                                        "rate_type_id": {
                                            "type": "integer",
                                            "description": "An ID for given room plan name",
                                        },
                                        "number_of_rooms": {
                                            "type": "integer",
                                            "description": "Number of rooms reserved for this room type",
                                        }
                                    },
                                    "required": ["room_type_id", "rate_type_id", "number_of_rooms"]
                                }
                            }
                        },
                        "required": ["json_type", "hotel_id","guest_name", "check_in", "check_out", "lines"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "agencyExists",
                    "description": "Checks whether travel agency exists in data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "json_type": {
                                "type": "integer",
                                "description": "Always 3"
                            },
                            "group_booking": {
                                "type": "integer",
                                "description": "whether this is a group booking or not (1 or 0)",
                            },
                            "agency_exist": {
                                "type": "integer",
                                "description": "whether the agency exists in data or not (1 or 0)",
                            },
                        },
                        "required": ["json_type", "group_booking", "agency_exist"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cancelConversation",
                    "description": "triggers when the customer ends the conversation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "json_type": {
                                "type": "integer",
                                "description": "Always -1"
                            },
                        },
                        "required": ["json_type"]
                    },
                }
            },
        ]
        self.data=data
        self.agents = agents
        self.systemRole = {
            "role": "system",
            "content":  sys_manage.base_insturctions(self.data, self.agents)
                }
        if(useChatGPT):
            from openai import OpenAI
            self.gClient =  OpenAI(api_key = "sk-proj-A8QEabiGhY556kM5Bki9T3BlbkFJTgeXFQ1YDXyXG0lJdPyS", organization="org-kRKVED7K5kqdCCYmM7LW87hn")
            self.model = "gpt-4o"
        else:
            from groq import Groq
            self.gClient =  Groq(api_key = api_key)
            self.model = "llama3-70b-8192"

        self.userMessage = ""
        self.response = None
        self.data = data
        self.gMessages = [
            
                self.systemRole
            ,
           
            
        ]
    def setUserMessage(self, userMessage):
        self.userMessage = userMessage
        self.prepareGMessages()
    
    def prepareGMessages(self):
        if(self.response!=None):
            self.gMessages.append(self.response)
        self.gMessages.append({
                "role": "user",
                "content": self.userMessage
            })
    def getResponse(self, tool_choice="auto"):
        completion = self.gClient.chat.completions.create(
        model=self.model,
        messages= self.gMessages,
        temperature=0.2,
        max_tokens=500,
        top_p=0.1,
        stream=True,
        stop=None,
        tools=self.tools,
        tool_choice=tool_choice
        )

        AIResponse = ""
        tool_calls = []
        tc = None
        for chunk in completion:
            delta = chunk.choices[0].delta

            if delta and delta.content:
                AIResponse +=delta.content or ""
                self.response = {
                    "role": "assistant",
                    "content": f"{AIResponse}",
                }

            elif delta and delta.tool_calls:
                tcchunklist = delta.tool_calls
                for tcchunk in tcchunklist:
                    if len(tool_calls) <= tcchunk.index:
                        tool_calls.append({"id": "", "type": "function", "function": { "name": "", "arguments": "" } })
                    tc = tool_calls[tcchunk.index]

                    if tcchunk.id:
                        tc["id"] += tcchunk.id
                    if tcchunk.function.name:
                        tc["function"]["name"] += tcchunk.function.name
                    if tcchunk.function.arguments:
                        tc["function"]["arguments"] += tcchunk.function.arguments
        if (tc != None):
            AIResponse = tc["function"]["arguments"]
            self.gMessages.append({
                "role": "function",
                "name": tc["function"]["name"],
                "content": tc["function"]["arguments"]
            })
        return AIResponse
    
    def clearHistory(self):
        self.response = None
        self.systemRole = sys_manage.base_insturctions(self.data, self.agents)
        self.gMessages =  [
                {
                    "role": "system",
                    "content":  self.systemRole 
                }
            
        ]


       