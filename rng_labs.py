import numpy as np

allLabs = ["BMP (includes Mg, Phos)", "LFTs", "CMP (BMP + LFTs)", "CBC only", "CBC with diff"]
           
    # future labs may include ABGs, coags, and others by request

def math(low, high):
    mean = (float(low) + float(high))/2
    std = (float(high) - float(low))/6
    return mean, std

def cbc(lab,normal):
    test = []
    result = []
    CBC = [
        ["WBC   ", 3.5, 10.8, 2],
        ["Hgb   ", 12, 16, 1],
        ["MCV   ", 80, 100, 1],
        ["MCHC  ", 32, 36, 1],
        ["RDW SD", 35, 46, 1],
        ["Plt   ", 150, 400, 0],
        ["MPV   ", 9.7, 12.3, 1],
        ["NRBC% ", 0, 0.1, 1]
    ]
    test = CBC    
    if lab == 4:     
        CBCdiff = [
            ["Neutro %", 50, 70, 1],
            ["Mono   %", 3.5, 9, 1],
            ["Eos    %", 1, 3, 1],
            ["Baso   %", 0, 2, 1],
            ["IG     %", 0, 1, 1]
        ]
        test.extend(CBCdiff)
            
    if normal == 1: 
        for row in test:
            mean, std = math(row[1], row[2])
            value = round(np.random.default_rng().normal(mean, std), row[3])
            result.append([row[0], value])
            
        # calculate Hct = (hgb * 100)/ MCHC
        while True:
            hct = 100 * result[1][1]/result[3][1]
            if hct < 36 or hct > 46: 
                mean, std = math(test[1][1], test[1][2])
                value = round(np.random.default_rng().normal(mean, std), test[1][3])
                result[1][1] = value
            else:
                result.insert(2, ["Hct   ", round(hct, 1)])
                break
        
        # calculate RBC = (hgb * 1000)/(MCHC * MCV)
        while True:
            rbc = 1000 * result[1][1]/(result[4][1] * result[3][1])
            if rbc < 4 or rbc > 5.2:
                mean, std = math(test[2][1], test[2][2])
                value = round(np.random.default_rng().normal(mean, std), test[2][3])
                result[3][1] = value  
            else:
                result.insert(1, ["RBC   ", round(rbc, 2)])
                break
        
        if lab == 4:
            wbc = result[0][1]
            
            # Lymphos = 100 - (neutros, monos, eos, basos, ig)
            while True:
                lymphs = 100 - (result[10][1] + result[11][1] + result[12][1] +
                               result[13][1] + result[14][1])
                if lymphs < 18 or lymphs > 42:
                    mean, std = math(test[8][1], test[8][2])
                    value = round(np.random.default_rng().normal(mean, std), test[8][3])
                    result[10][1] = value  
                else: 
                    result.insert(11, ["Lympho %", round(lymphs, 0)])
                    break
            
            # get absolute cell counts
            for i in range(10,16):
                name = result[i][0].replace("%", "#")
                absval = round(wbc * result[i][1]/100, 2)
                result.append([name, absval])
            
    # deal with some abnormal values        
    else: 
        n_mean = n_std = 0
        for row in test:
                        # check if data element is normal
            nl = input("Is " + row[0] + " normal? (Y/N)")
            
            if nl in ("Y", "y", "yes", "Yes"):
                mean, std = math(row[1], row[2])
                value = round(np.random.default_rng().normal(mean, std), row[3])
                result.append([row[0], value])
                
            else:
                # ask for mean and std deviation to use
                low = input("Enter lowest desired value: ")
                if not low.isdecimal():
                    low = row[1]
                    print(low)
                high = input("Enter highest desired value: ")
                if not high.isdecimal():
                    high = row[2]
                if float(high) <= float(low):
                    high = row[2]
                    if float(high) <= float(low): 
                        low = row[1]
                mean, std = math(low, high)
                if row[0] == "Neutro %":
                    n_mean = mean
                    n_std = std
                value = round(np.random.default_rng().normal(mean, std), row[3])
                result.append([row[0], value])

        hct = 100 * result[1][1]/result[3][1]
        result.insert(2, ["Hct   ", round(hct, 1)])

        rbc = 1000 * result[1][1]/(result[4][1] * result[3][1])
        result.insert(1, ["RBC   ", round(rbc, 2)])

        if lab == 4:
            wbc = result[0][1]
            
            while True:
                # Lymphos = 100 - (neutros, monos, eos, basos, ig)
                lymphs = 100 - (result[10][1] + result[11][1] + result[12][1] +
                                result[13][1] + result[14][1])
                if lymphs < 0:
                    value = round(np.random.default_rng().normal(n_mean, n_std), 1)
                    result[10][1] = value
                else:
                    result.insert(11, ["Lympho %", round(lymphs, 0)])
                    break
            
            # get absolute cell counts
            for i in range(10,16):
                name = result[i][0].replace("%", "#")
                absval = round(wbc * result[i][1]/100, 2)
                result.append([name, absval])
    print("\nResults:")
    for row in result:
        print(row[0] + ": " + str(row[1]))
    return


def gen(lab,normal):
    # data element reference range and decimals
    BMP = [
        ["Na   ", 136, 145, 0],
        ["K    ", 3.4, 5, 1],
        ["Cl   ", 97, 108, 0],
        ["CO2  ", 21, 32, 0],
        ["BUN  ", 6, 20, 0],
        ["Cr   ", 0.6, 1.1, 2],
        ["Glu  ", 70, 99, 0],
        ["Ca   ", 8.6, 10.2, 1], 
        ["Mg   ", 1.6, 2.6, 1],
        ["Phos ", 2.4, 4.7, 1]
    ]
    
    LFT = [
        ["Prot    ",6.4,8.2,1],
        ["Alb     ",3.5,4.7,1],
        ["T Bili  ",0.3,1.2,1],
        ["D Bili  ",0,0.3,1],
        ["AST     ",10,41,0],
        ["ALT     ",0,60,0],
        ["Alk Phos",42,98,0],
    ]
    
    test = []
    result = []
    
    # set test as panel selected
    if lab == 0:
        test = BMP
    elif lab == 1:
        test = LFT
    elif lab == 2:
        test = BMP
        test.extend(LFT)
    else:
        print("Error: unrecognized test panel")
        return 1
    
    # entire panel is normal
    if normal == 1: 
        for row in test:
            mean, std = math(row[1], row[2])
            value = round(np.random.default_rng().normal(mean, std), row[3])
            result.append([row[0], value])
            
    else:
        for row in test: 
            
            # check if data element is normal
            nl = input("Is " + row[0] + " normal? (Y/N)")
            
            if nl in ("Y", "y", "yes", "Yes"):
                mean, std = math(row[1], row[2])
                value = round(np.random.default_rng().normal(mean, std), row[3])
                result.append([row[0], value])
                
            else:
                # ask for mean and std deviation to use
                low = input("Enter lowest desired value: ")
                high = input("Enter highest desired value: ")
                mean, std = math(low, high)
                value = round(np.random.default_rng().normal(mean, std), row[3])
                result.append([row[0], value])
    print("\nResults:")
    for row in result:
        print(row[0] + ": " + str(row[1]))
    return

def main():
    # choose a laboratory panel
    print("Choose an option below:")
    for i in range(len(allLabs)):
        print("%d: %s" % (i+1, allLabs[i]))
    lab = int(input())-1
    nl = input("Entire panel normal? (Y/N)")
    if nl in ("Y", "y", "yes", "Yes"):
        normal = 1
    else: 
        normal = 0
    if lab in (3, 4):
        cbc(lab, normal)
    else:
        gen(lab, normal)
    # check for more work
    more = input("Generate more labs? (Y/N)")
    if more in ("Y", "y", "yes", "Yes"):
        main()
    else:
        print("Thank you for using random lab generator!")
        return 

main()
            