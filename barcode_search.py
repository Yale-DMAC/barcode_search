#/usr/bin/python3
#~/anaconda3/bin/python

import requests, csv, json, logging, time, subprocess, os, sys


#quit at any time? or restart at any time?
#more newlines?

def keeptime(start):
    elapsedtime = time.time() - start
    m, s = divmod(elapsedtime, 60)
    h, m = divmod(m, 60)
    logging.debug('Total time elapsed: ' + '%d:%02d:%02d' % (h, m, s) + '\n')

def open_outfile(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filepath])

def error_log():
    if sys.platform == "win32":
        logger = '\\Windows\\Temp\\error_log.log'
    else:
        logger = '/tmp/error_log.log'
    logging.basicConfig(filename=logger, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    return logger

def login():
    try:
        url = input('Please enter the ArchivesSpace API URL: ')
        username = input('Please enter your username: ')
        password = input('Please enter your password: ')
        auth = requests.post(url+'/users/'+username+'/login?password='+password).json()
        #if session object is returned then login was successful; if not it failed.
        if 'session' in auth:
            session = auth["session"]
            h = {'X-ArchivesSpace-Session':session, 'Content_Type': 'application/json'}
            print('\nLogin successful!\n')
            logging.debug('Success!')
            return (url, h)
        else:
            print('\nLogin failed! Check credentials and try again\n')
            logging.debug('Login failed')
            logging.debug(auth.get('error'))
            u, heads = login()
            return u, heads
    except:
        print('\nLogin failed! Check credentials and try again!\n')
        logging.exception('Error: ')
        u, heads = login()
        return u, heads

#Open a CSV in reader mode
def opencsv():
    try:
        input_csv = input('Please enter path to CSV: ')
        file = open(input_csv, 'r', encoding='utf-8')
        csvin = csv.reader(file)
        next(csvin, None)
        return (input_csv, csvin)
    except:
        logging.exception('Error: ')
        logging.debug('Trying again...')
        print('\nCSV not found. Please try again.\n')
        i, c = opencsv()
        return (i, c)

#Open a CSV file in writer mode
def opencsvout(infilename):
    try:
        output_csv = infilename + '_outfile.csv'
        fileob = open(output_csv, 'a', encoding='utf-8', newline='')
        csvout = csv.writer(fileob)
        return (output_csv, fileob, csvout)
    except:
        logging.exception('Error: ')
        print('\nError creating outfile. Please try again.\n')
        i, f, c = opencsvout()
        return (i, f, c)

def search_barcodes(log_file):
    starttime = time.time()
    logging.debug('Connecting to ArchivesSpace API...')
    api_url, headers = login()
    logging.debug('Opening barcode file...')
    ininput_string, csvfile = opencsv()
    logging.debug('Opening output file...')
    input_string, fileobject, csvoutfile = opencsvout(ininput_string)
    csv_headers = ['barcode', 'series', 'identifier', 'title', 'container_profile', 'container_number']
    csvoutfile.writerow(csv_headers)
    print('\nPlease wait a moment...')
    for row in csvfile:
        barcode = row[0]
        try:
            logging.debug('Searching ' + barcode)
            search = requests.get(api_url + '/repositories/12/top_containers/search?q=barcode_u_sstr:' +  barcode, headers=headers).json()
            #Searching identifier and title, which are both required fields
            identifier = search['response']['docs'][0]['collection_identifier_stored_u_sstr'][0]
            title = search['response']['docs'][0]['collection_display_string_u_sstr'][0]
            #Checking for a series
            if 'series_identifier_stored_u_sstr' in search['response']['docs'][0].keys():
                series = search['response']['docs'][0]['series_identifier_stored_u_sstr'][0]
            else:
                series = 'no_series'
                logging.debug('No series. ' + str(search['response']['docs'][0]))
            #Checking for container info
            record_json = json.loads(search['response']['docs'][0]['json'])
            #Indicator is a required field
            container_number = record_json['indicator']
            #Checking for a container profile
            if 'container_profile_display_string_u_sstr' in search['response']['docs'][0].keys():
                container_profile = search['response']['docs'][0]['container_profile_display_string_u_sstr'][0]
            else:
                container_profile = 'no_container_profile'
                logging.debug('No container profile. ' + str(search['response']['docs'][0]))
            #Writing everything to the output CSV
            newrow = [barcode, series, identifier, title, container_profile, container_number]
            csvoutfile.writerow(newrow)
        except:
            print('Error! Could not retrieve record ' + str(row))
            logging.exception('Error: ')
            logging.debug(str(search))
            row.append('ERROR')
            csvoutfile.writerow(row)
    fileobject.close()
    keeptime(starttime)
    logging.debug('All Done!')
    print('\nAll Done!')
    open_outfile(input_string)
    open_outfile(log_file)
    #print("\n\nCredit: program icon was made by http://www.freepik.com on https://www.flaticon.com/ and is licensed by Creative Commons BY 3.0 (CC 3.0 BY")

if __name__ == "__main__":
    print('''\n\n
             #################################################
             #################################################
             ####################  HELLO!  ###################
             #################################################
             #####  WELCOME TO THE LSF TRANSFER BARCODE  #####
             #####               LOOKUP TOOL!            #####
             #################################################
             #################################################
             \n\n''')
    time.sleep(1)
    print("                            Let's get started!\n\n")
    time.sleep(1)
    barcode_logfile = error_log()
    search_barcodes(barcode_logfile)