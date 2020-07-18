# sql_threads = []
        # sql_results = [None]

        # sql_threads.append(threading.Thread(target=sqlcommands.get_clusters, args=(sql_results, len(sql_threads))))
        # sql_threads.append(threading.Thread(target=sqlcommands.get_Standalone_servers, args=(sql_results, len(sql_threads))))

        # for i in sql_threads:
        #     i.start()

        # conversion_threads = []
        # conversion_results = [None]

        # loop = True
        # while loop:
            
        #     all_done = True
        #     for i in sql_results:
        #         if type(i) == str and i != 'Done':
        #             all_done = False
        #     if all_done: loop = False

        #     results_back = [x for x in sql_results if ('Wait' not in x) and ('Done' not in x)]

        #     for result in results_back:
        #         conversion_threads.append(threading.Thread(target=self.sqlreturn_to_tabledata, args=('Cluster', result, conversion_results, 0) ))
        #         conversion_threads[-1].start()
        #         sql_results[sql_results.index(result)] = 'Done'

        # for i in sql_threads:
        #     i.join()

        # for j in conversion_threads:
        #     j.join()
        
        # headers, objectdata = conversion_results[0]

        # headers = []
        # objectdata = []
        # for heads, data in sql_results:
            
        #     for head in heads:
        #         if head not in headers: headers.append(head)
        #     objectdata += data