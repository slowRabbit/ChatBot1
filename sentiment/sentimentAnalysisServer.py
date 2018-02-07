from flask import request, jsonify, json, Response, render_template
import pygal
import SentimentAnalyzer
from pygal.style import LightenStyle



class SentimentAnalysisClass:
    
    def __init__(self):
        self.allChatList = []
        self.allChatDictionary = {}
        self.isUpdated = 0
    
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
        
    def setUpdated(self, booleanUpdated):
        self.isUpdated = booleanUpdated
    
    def isUpdated(self):
        return self.isUpdated
    
    
    def postChat(self,chat, time):
        
        #response = request.get_json()
        #chat = response.get('chat')
        #time = response.get('time')
        
        Chat = SentimentAnalyzer.getSentimentAnalyzedChat(chat, time)
        self.allChatList.append(Chat)
    
    
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
    
    def getSentimentAnalysisWebPage(self):
        #graph = pygal.Line()
        graph_score_style = LightenStyle('#0288D1')
        graph_magnitude_style = LightenStyle('#AFB42B')
        graph_factor_style = LightenStyle('#FFA000')
        
        graph_score = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_score_style)
        graph_magnitude = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_magnitude_style)
        graph_factor = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_factor_style)
        label_list = []
        factor_list = []
        magnitude_list = []
        score_list = []
                
        for Chat  in  self.allChatList:
            label_list.append(Chat.getTime())
            score_list.append(float(Chat.getScore()))
            magnitude_list.append(float(Chat.getMagnitude()))
            factor_list.append(float(Chat.getFactor()))
                
        graph_score.title = ' Score VS Time '
        graph_magnitude.title = ' Magnitude VS Time '
        graph_factor.title = ' Factor VS Time '
        
        graph_score.x_labels = label_list
        graph_magnitude.x_labels = label_list
        graph_factor.x_labels = label_list
        
        graph_score.add('Score', score_list)
        graph_magnitude.add('Magnitude', magnitude_list)
        graph_factor.add('Factor', factor_list)
        
        graph_data_score = graph_score.render_data_uri()
        graph_data_magnitude = graph_magnitude.render_data_uri()
        graph_data_factor = graph_factor.render_data_uri()
                
        return render_template("sentimentanalysis.html", graph_data_score = graph_data_score, graph_data_magnitude = graph_data_magnitude, graph_data_factor = graph_data_factor)

    def getFactorDataForGraph(self):
        #graph = pygal.Line()
        graph_score_style = LightenStyle('#0288D1')
        graph_magnitude_style = LightenStyle('#AFB42B')
        graph_factor_style = LightenStyle('#FFA000')
        
        graph_score = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_score_style)
        graph_magnitude = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_magnitude_style)
        graph_factor = pygal.StackedLine(fill=True, interpolate='cubic', style=graph_factor_style)
        #graph_factor = pygal.StackedLine(fill=True, interpolate='cubic', style=DarkStyle)
        
        label_list = []
        factor_list = []
        magnitude_list = []
        score_list = []
                
        for Chat  in  self.allChatList:
            label_list.append(Chat.getTime())
            score_list.append(float(Chat.getScore()))
            magnitude_list.append(float(Chat.getMagnitude()))
            factor_list.append(float(Chat.getFactor()))
                
        graph_score.title = ' Score VS Time '
        graph_magnitude.title = ' Magnitude VS Time '
        graph_factor.title = ' Factor VS Time '
        
        graph_score.x_labels = label_list
        graph_magnitude.x_labels = label_list
        graph_factor.x_labels = label_list
        
        graph_score.add('Score', score_list)
        graph_magnitude.add('Magnitude', magnitude_list)
        graph_factor.add('Factor', factor_list)
        
        graph_data_score = graph_score.render_data_uri()
        graph_data_magnitude = graph_magnitude.render_data_uri()
        graph_data_factor = graph_factor.render()
                
        return graph_data_factor
