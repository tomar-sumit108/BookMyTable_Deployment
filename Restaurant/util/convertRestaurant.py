from CommentRating.get import get_reviews
from collections import defaultdict
import operator
def convert_restaurant(cursor, rows,reviews=False,meta="NO"):
        for row in rows:
                cursor.execute("SELECT * FROM Location where id=%s",
                        row['location_id'])
                loc = cursor.fetchall()
                row['location'] = loc[0]

                cursor.execute("SELECT * FROM Day where restaurant_id=%s",row['id'])
                days=cursor.fetchall()
                row['days']=days[0]
                del row['days']['restaurant_id']
                
                
                
                cursor.execute("SELECT * FROM Slot where restaurant_id=%s",row['id'])
                slots=cursor.fetchall()
                row['slots']=slots
                del row['timings']

                if reviews:
                        row['reviews']=get_reviews(resId=row['id']).json
                
                del row['location_id']

        if meta!="NO" and not reviews and len(rows)!=0:
                dic={}
                dic['highlights']={}
                dic['establishments']={}
                dic['cuisines']={}
                for row in rows:
                        est=row['establishment'].split(", ")
                        cui=row['cuisines'].split(", ")
                        hlt=row['highlights'].split(", ")
                        for ee in est:
                                if ee and (not ee in dic['establishments']):
                                        dic['establishments'][ee]=0
                                if ee:
                                        dic['establishments'][ee]=dic['establishments'][ee]+1
                        for hh in hlt:
                                if hh and (not hh in dic['highlights']):
                                        dic['highlights'][hh]=0
                                if hh:
                                        dic['highlights'][hh]=dic['highlights'][hh]+1
                        for  cc in cui:
                                if cc and (not cc in dic['cuisines']):
                                        dic['cuisines'][cc]=0
                                if cc:
                                        dic['cuisines'][cc]=dic['cuisines'][cc]+1
                

                print("meta is ",meta)
                if meta=='highlights':
                        return dic['highlights']
                if meta=='establishments':
                        return dic['establishments']
                if meta=='cuisines':
                        return dic['cuisines']
                return rows
        return rows

        
        