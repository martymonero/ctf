# Misc/Numbers Game - 206 Points

It's been a long time since I attended my last CTF (October 2017). That's why I set my goal for the RCTF moderately low. I wanted to solve at least one challenge that wasn't the easiest. (I am looking at you Misc/Git)

I ended up working on the Numbers Game Challenge.

You were given a Host and Port and needed to connect to play the little game.

You were greeted with this message:

```
sha256(****+yHn1M1ZBTLVP2zQh) == 1fdfcd161d85b245030e4dd1e5e0fae9b11afc45a4b048667503009a77ccfa19
Give me XXXX:
```

First task was to brute force 4 characters of an input that was hashed via SHA256.


I quickly wrote a bruter forcer for this in Python and was ready to go...But it didn't work.

I lost at least an hour because I considered the "+" as a character of the known part...Thats why I added all special password characters into the Brute Force Character Set.

![Are you kidding me](http://i0.kym-cdn.com/photos/images/masonry/000/259/943/694.png
)

My typical problem... making things too complicated :D

After removing the "+" and also removing the special characters from my Brute Force Character Set, the script did not only perform way faster, it even worked :D I reconnected to the Host to input the XXXX ...only to realize that the Hashes and the Known Parts change on every reconnect...

Ok no problem. I extended the python script to open the socket itself and extract the Known Part and the Target Hash.

Yay...now give me the flag!

Damn. Stage 2...

```
  o__ __o             o__ __o    ____o__ __o____   o__ __o__/_
 <|     v\           /v     v\    /   \   /   \   <|    v
 / \     <\         />       <\        \o/        < >
 \o/     o/       o/                    |          |
  |__  _<|       <|                    < >         o__/_
  |       \       \                    |          |
 <o>       \o       \         /         o         <o>
  |         v\       o       o         <|          |
 / \         <\      <\__ __/>         / \        / \



In every round of the game, I'll choose some different numbers from the figure interval. You are required to guess those numbers,ofc so does the order of them.
On each surmise of yours, 2 numbers will be told as a hint for you, but you need to speculate the fuctions of these 2 figures. (XD
GLHF

================== round 1 ==================
Give me 4 numbers, in[0, 10), You can only try 6 times
0 0 0 0
Nope. 0, 0
1 1 1 1
Nope. 0, 0
2 2 2 2
Nope. 1, 0
2 1 1 1
Nope. 1, 0
1 2 1 1
Nope. 0, 1
1 1 2 1
Nope. 0, 1
You lose, Correct answer is 2 5 6 7 .Bye.
```

After playing the game manually for a while I knew that I needed to create a script to solve it because the socket had a timeout and you needed to be quick. Also the intro indicated that there were more rounds. I figured the two hints were telling me which numbers were right and at the right spot and which numbers were right and at the wrong spot. This turned out to be right.

After googling "4 out of 10 6 tries" I ended up in math forums and the algorithm vortex of Donald Knuth. The Game I was playing was similiar to "MasterMind". An apparently very popular game which I had never played and the best way to solve it was by using Donald Knuth's "Five Guess Algorithm".

First thing I did was to check for existing github repositories that had already invented the wheel. I found a couple of scripts but they often contained convoluted code. This was not enough. I wanted to fully understand what I was doing. So I ended up recreating the MasterMind Game in Python :D

Afterwards I implemented 90% of the Five Guess Algorithm. This was already quite satisfying to watch. Check my mastermind-codebreaker.py to see it in action.

```
python mastermind-codebreaker.py
Secret: [2, 7, 9, 5]
(0, 0, 1, 1)
[0, 0]
4096 Elements left
(3, 8, 9, 3)
[1, 0]
682 Elements left
(6, 8, 4, 2)
[0, 1]
157 Elements left
(3, 7, 6, 5)
[2, 0]
9 Elements left
(2, 7, 9, 5)
[4, 0]
You have won the game!
```

Now it was time to extend the [numbers-game.py](numbers-game.py) to finally get the Flag.

(Tbh, at this point I even got one lucky try and got the flag on the second try. Maybe I should play the lottery!) 

Turns out the game has even 8 rounds! But I figured, that my algorithm wasn't optimal as the normal Five-Guess Algorithm would implement a min max technique (Step 6) that would also consider not possible codes in order to find out which next guess would eliminate the most elements from S. This concept is hard to grasp at first and all the articles on the web are quite confusing. I can recommend this whitepaper if you want dig deeper into the subject matter: [https://arxiv.org/pdf/1305.1010.pdf](https://arxiv.org/pdf/1305.1010.pdf)

And I was right: After executing again and again my solver almost always needed 7 tries. I needed a different approach. After implementing step 6 of Knuths algorithm I have realized that this was extremely slow. Perhaps my algorithm wasn't optimal. (Should be a tree approach instead of two foreach loops, I guess). You can find my shot at it in the [codebreaker script](mastermind-codebreaker.py). Feel free to improve and let me now how you did it!

As the RCTF organizers even used the numbers 0-9 and the normal Mastermind algorithms always talk about 1-6 or A-E and the famous 1296 possibilities (in our case it would be 9999), I thought that they must have changed something to make it solvable.
Then it jumped at me. Their solutions never had duplicate numbers in them!

I changed my script to not allow duplicate numbers in a guess and was good to go. (I know that itertools.permutations is the right way but I was quite exhausted at this point :D)

Now the success rate of the solver was ok and it got the flag basically every third try.

```
RCTF{0lD_GaM3_nAmed_Bu11s_4nd_C0ws}
```

In the end I found out that I should only have googled "cows and bulls python" to save hours of research :D


![Table Flip](http://i0.kym-cdn.com/entries/icons/original/000/006/725/desk_flip.jpg
)



PS: But then I wouldn't have learned anything :) 
