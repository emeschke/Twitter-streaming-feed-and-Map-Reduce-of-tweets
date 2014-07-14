from mrjob.job import MRJob
from timeConvert import get_epoch_minute
'''This code uses Hadoop Streaming and the MRJob package to read in lines from
Hadoop Streaming stdin, process, and output a key value pair from the reducer.

Mapper: Split string by ",".  Convert time.  key=time, value=other_info
Reducer: Aggregate on count(values), followers, mentions>0.  Ouput key=time,
value=count_total, count_mentions, average_followers.

Input to MRJob is a text file of the form:
datetime,number of followers,number of mentions
Ex: '2014-06-05 15:10:30,1069,3'

MRJob documentation:
https://pythonhosted.org/mrjob/
'''

class CSVProtocol(object):
    #Override the write function to format the key, value delimited by ","
    def write(self, key, value):
        return '%s,%s' % (key, value)

class ParseMinutesTwitter(MRJob):
    #Set output to the protocol defined above.    
    OUTPUT_PROTOCOL = CSVProtocol
    
    def mapper(self, _, line):
        #Split the input line.        
        line = line.split(",")
        #Call the user defined function that transforms the time to Epoch min        
        key = get_epoch_minute(line[0])
        #Make sure it was a valid time (and therefore a valid line to process)
        if key is not -1:        
            #Write the key, tuple(# followers, # mentions) to the map output.
            yield (key,(int(line[1]), int(line[2])))  

    def reducer(self, key, values):
        #Variables for total count, total mentions and total followers.        
        count_total = 0
        count_mentions = 0
        total_followers = 0
        #Iterate through the values list associated with this key.        
        for val in values:
            #Increment total by 1, total followers by the # followers for this value.            
            count_total += 1
            total_followers += val[0]
            #Check if there are mentions, if so increment the count_mentions.            
            if val[1] > 0:
                count_mentions += 1
        #Calculate average followers.        
        average_followers = float("%.1f" % (1.0*total_followers/count_total))        
        #Create an output tuple.        
        output_tuple = (count_total,count_mentions,average_followers)
        #Yield the key, output_tuple (formatting the output_tuple as a CSVstring.)        
        yield (key, str(output_tuple).strip("()").replace(" ",""))
            


if __name__ == '__main__':
    ParseMinutesTwitter.run()