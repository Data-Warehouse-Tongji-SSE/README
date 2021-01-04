import json

data_path = "D:\cmd\data.txt"
output_path = "D:\cmd\outputdata.txt"
with open(data_path, "r", encoding="utf-8") as jsonfile:
    index = 0
    while True:
        current_line = jsonfile.readline()
        if current_line == '':
            break
        current_line = current_line.strip()
        line_text = json.loads(current_line)
        self_line=""
        t_lo=line_text["pid"]
        try: 
            self_id = line_text["productDetail"]
            self_line=self_id["MPAA rating"]        
        except:
            try:
                self_id=line_text["primeMeta"]
                self_line=self_id["Genres"]
            except:
                continue
        if index % 2500 == 0:
            print('Current Index: ', index)
        if self_line!="":
            
        #try: 
          #  for asin in line_text["additionalOptions"]:
           #     if asin in id_list_not_404.id_list:
            #        myUnionFind.union(self_id, asin)
        #except:pass   
         index += 1
with open(output_path, "a", encoding="utf-8") as outputfile:
    print('"'+t_lo+'",', file=outputfile)
print('Final Index: ', index)