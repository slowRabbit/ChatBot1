from flask import jsonify, json, Response
import SentimentAnalyzer



class SentimentAnalysisClass:
    
    def __init__(self):
        self.allChatList = []
        self.allChatDictionary = {}
        self.replyEntity = 'bot'
    
    def getAllChats(self):
    
        if len(self.allChatList) is 0:
            return '-1'
        
        else :
            result = '{"ChatList" :['
            for Chat  in  self.allChatList:
                result = result + json.dumps({
                            'chat': Chat.getChat(),
                            'time': Chat.getTime(),
                            'score' : Chat.getScore(),
                            'magnitude' : Chat.getMagnitude(),
                            'factor' : Chat.getFactor()
                            }, indent =2) +','
            result = result + ']}'
            res1 = result[:-3]
            res2 = result[-2:]
            #return res1+res2
            return Response(res1+res2, mimetype='application/json')
        
    
    def postChat(self,chat, time):
        
        #response = request.get_json()
        #chat = response.get('chat')
        #time = response.get('time')
        
        Chat = SentimentAnalyzer.getSentimentAnalyzedChat(chat, time)
        self.allChatList.append(Chat)
        
        #now we will check the sentiment of chat message that we have received
        if (float(Chat.getFactor()) <= -0.70):
            self.replyEntity = 'agent'
        
        return jsonify({'AddedChat':
                {
                        'chat': Chat.getChat(),
                        'time': Chat.getTime(),
                        'score' : Chat.getScore(),
                        'magnitude' : Chat.getMagnitude(),
                        'factor' : Chat.getFactor()
                        }
            })
        
    def resetChatList(self):
            self.allChatList[:] = []
            return jsonify({'result':'All chats removed'})
        
    def getAllChatListForWebPage(self):
        chat_list = []
        time_list = []
        sentiment_list = []
        
        for Chat  in  self.allChatList:
            chat_list.append(Chat.getChat())
            time_list.append(Chat.getTime())
            sentiment_list.append(Chat.getFactor())
        
        return jsonify({'time_list' : time_list, 
                        'chat_list' : chat_list,
                        'sentiment_list' : sentiment_list
                        })
    
    def getInitialGraphDataJson(self):
         label_list = []
         #factor_list = []
         positive_factor_list = []
         negetive_factor_list = []
         positive_chat_count = 0
         negetive_chat_count = 0
         all_chat_sentiment_sum = 0
         
         for Chat  in  self.allChatList:
            label_list.append(Chat.getTime())
            currentChatFactor = float(Chat.getFactor())
            all_chat_sentiment_sum = all_chat_sentiment_sum + currentChatFactor
            
            if(currentChatFactor >= 0):
                #when chat is positive
                positive_factor_list.append(currentChatFactor)
                negetive_factor_list.append(0)
                positive_chat_count +=1
                
            else :
                #when chat is negetive
                positive_factor_list.append(0)
                negetive_factor_list.append(currentChatFactor)
                negetive_chat_count +=1
            
         total_chats = len(self.allChatList)
         if (total_chats  == 0):
             avgSentiment = 0
         else:
             avgSentiment = float(all_chat_sentiment_sum / total_chats)
         #returning all data to ajax call for UI update
         return jsonify({ 'labels':label_list, 
                          'positive_factor_list':positive_factor_list, 
                          'negetive_factor_list':negetive_factor_list,
                          'positive_chat_count': positive_chat_count,
                          'negetive_chat_count': negetive_chat_count,
                          'total_chat_count' : total_chats,
                          'average_sentiment' : avgSentiment
                          })
    
    def setReplyEntityToAgent(self):
        self.replyEntity = 'agent'
        
    def setReplyEntityToBot(self):
        self.replyEntity = 'bot'
        
    def getReplyEntity(self):
        return self.replyEntity
    
    def getNegetiveChatCount(self):
        negetive_chat_count = 0
        for Chat  in  self.allChatList:
            currentChatFactor = float(Chat.getFactor())
            if(currentChatFactor < 0):
                negetive_chat_count +=1
        return negetive_chat_count
    
    def getAvgChatSentiment(self):
        all_chat_sentiment_sum = 0
        for Chat  in  self.allChatList:
            currentChatFactor = float(Chat.getFactor())
            all_chat_sentiment_sum = all_chat_sentiment_sum + currentChatFactor
            
        total_chats = len(self.allChatList)
        if (total_chats  == 0):
             avgSentiment = 0
        else:
             avgSentiment = float(all_chat_sentiment_sum / total_chats)
        
        return avgSentiment
    