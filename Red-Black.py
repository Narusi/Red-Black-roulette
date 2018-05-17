import random
import pandas as pd
import matplotlib.pyplot as plt

oMoney = float(input("How much money would You gamble on Black & Red strategy?\n"))
oBet = float(input("What's your starting bet?\n"))
y = int(input('How many simulations shall we run?\n'))

bet = oBet
playerChoise = ['Red','Black']

player = random.choice(playerChoise)
casino = ''

result = ['Red','Black','Zero']
prob = [18/37,18/37,1/37]
totalFigs = []
rands = []

print("\nStarting the game simulation:\n")
x = 1

while x < y:
    if (100*x/y)%1 == 0:
        print('Running simulation: {}%'.format(round(100*x/y)))
        
    maxMoney = 0.00
    maxBet = 0.00
    rounds = 0
    bigLoss = 0.00
    money = oMoney
 
    while money > 0:
        rounds += 1
        casino = random.choices(result, weights=prob)
        win = casino[0] == player
        
        if win:
            rands.append([player, casino[0], 1])
        else:
            rands.append([player, casino[0], 0])
        
        if win:
            money = money + bet
                
            if bet>maxBet:
                maxBet = bet
            
            bet = oBet
            
            if player == 'Red':
                player = 'Black'
            else:
                player = 'Red'
                
        else:
            money = money - bet
            
            if bet > bigLoss:
                bigLoss = bet
            
            if bet * 2 <= money:
                bet = bet * 2
            else:
                bet = money
        
        if money > maxMoney:
            maxMoney = money

        

    totalFigs.append([maxMoney, maxBet, bigLoss, rounds])
    x+= 1
    
results = pd.DataFrame(totalFigs, columns=list(['MAX money','Biggest Loss','MAX bet','Rounds']), dtype='float64')
results['Rounds'].astype('int64')

randoms = pd.DataFrame(rands, columns=list(['Player choice', 'Casino', 'W/L']))
randoms['W/L'].astype('int64')

results.to_csv('D:\Development\Python Projects\Red&Black\Red&Black outcomes.csv', sep=';',index=False, decimal=',')
randoms.to_csv('D:\Development\Python Projects\Red&Black\Red&Black details.csv', sep=';',index=False, decimal=',')
    
print('\nOn average players loose their money in {} rounds. \nHighest increase in player total money is around {}% and bet won by {}% while largest bet lost by {}%\n'.format(round(results['Rounds'].mean()),abs(round(100*(1-results['MAX money'].mean()/oMoney))),abs(round(100*(1-results['MAX bet'].mean()/oBet))),abs(round(100*(1-results['Biggest Loss'].mean()/oBet)))))
print('Overall STDs per measurements: /nTotal money pool: {}% \nLargest won bets: {}% \nLargest lost bets: {}%\n'.format(abs(round(results['MAX money'].std())),abs(round(results['MAX bet'].std())),abs(round(results['Biggest Loss'].std()))))

print('In total player outplayed Casino {}% of the time.'.format(round(100*randoms['W/L'].sum()/randoms['Player choice'].count())))

print('Player winnings by color:')
pBlack = randoms[randoms['Player choice'] == 'Black']
pRed = randoms[randoms['Player choice'] == 'Red']
print('Black: {}%'.format(100*round(pBlack['W/L'].mean(), 3)))
print('Red: {}%'.format(100*round(pRed['W/L'].mean(), 3)))