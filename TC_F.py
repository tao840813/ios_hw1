# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 15:05:40 2018

@author: theodore
"""

def TC(file):

    filename = file

    # Read input file
    
    with open(filename, "r") as inputfile:
        seq = inputfile.read()

    # Prepare POST data that will sent to T-Coffee server
    
    post_data = {
        'seqs': seq,
        'output': 'phylip,score_ascii,fasta_aln,clustalw_aln,score_html',
        'letter':'upper',
        'seqnos':'off',
        'outorder':'input',
        'msa_max_len':'80',
        'email':''
        }

    encodedData = urllib.parse.urlencode(post_data).encode(encoding='ascii')    

    # Send post request to T-Coffee
    
    req = urllib.request.Request(url = 'http://tcoffee.vital-it.ch/apps/tcoffee/do:regular', data = encodedData)
    resp = urllib.request.urlopen(req)

    # Convert response data to string
    respStr = str(resp.read())

    # Extract key from response
    # If we can't find key, that might be something wrong!!
    
    match = re.search("result\?rid=([^\"]+)" , respStr)
    
    if(match):
        key = match.group(1)
        print('Our access key: ' + str(key))
    else:
        print("No access key found! Something goes wrong...")
        return -1;

    # Polling for result

    resUrl = 'http://tcoffee.vital-it.ch/data/%s/result.phylip' % key
    resUrl2 = 'http://tcoffee.vital-it.ch/data/%s/result.fasta_aln' %key

    print('Getting result')

    retry = 1;
    while True: 

        try:
            r = urllib.request.Request(resUrl)
            resResp = urllib.request.urlopen(r)
            
            r2 = urllib.request.Request(resUrl2)
            resResp2 = urllib.request.urlopen(r2)
            break
        except urllib.error.HTTPError:
            print('Server returned 404   Retrying... Attempts %d' % retry)
            retry = retry + 1
            time.sleep(10)


    result = str(resResp.read().decode('utf-8'))
    result2 = str(resResp2.read().decode('utf-8'))
    # Output our result
    
    with open('%s.phylip' % key, 'w') as f:
        f.write(result)
    with open('%s.fasta' % key, 'w') as f2:
        f2.write(result2)
    print('Successfully write result to %s.txt & A %s.txt' % (key,key))
    #get the sequence
    with open('%s.phylip' %key,'r') as fin:
        for line in fin:
            print(line)
    return key
TC('test5.fasta')