# Birthday-Attack
From the [Open Learning page](https://www.openlearning.com/unswcyber/courses/security-engineering-23t3/activities/birthday/?cl=1)
Code inspired by Yash Dudam ([OL post](https://www.openlearning.com/u/yashdudam-s0swsx/blog/BirthdayAttack/), [GitHub](https://github.com/YashDudam/birthday-attack/blob/main/birthday_attack.py))

Currently a pretty simple Python solution. Could improve with:
- [Multiprocessing](https://www.openlearning.com/u/liamsmith-s124mp/blog/BirthdayAttack/)/multithreading
- Put (or don't put) a single space at the end of each line for a more normal looking output - each line essentially becomes a bit (0/1 for off/on for no space/space)
- Using a faster language, e.g C++ or Rust
- Other optimisations? [Lucas](https://www.openlearning.com/u/lucasharvey-s0t5ay/blog/BirthdayAttack16Characters/) and Daniel did some dark magic to get 16 characters

Timings (M2 Pro Macbook Pro):
- 6 character matching: 0.104 s
- 7: 1.247
- 8: 53.566 s
- 9: 2:03.99 m:ss
- 10: (killed my RAM)

## Birthday Attack

When hashes are used assure the integrity of a message what could be very bad is if attackers could find or create collisions with a feasible amount of work.  

This activity is to create two files with very different messages which have the same hash.  A nightmare for anyone relying upon the hash for integrity.  You could of course carry out a second preimage attack, but that will be slow.  Much smarter to carry out a birthday attack and only do the squareroot of the amount of work.

## Task
I have asked you to type up a secret confession for me and give it to me as an ASCII file.  I will then SHA256 the ASCII file and publish the last few hex digits of the hash as a public integrity check (I should of course publish it all not just the last few digits - but that would make this exercise too time consuming for you!).  However I will keep the confession secret for now.  It is to be revealed later.

However a nameless billionaire has bribed you to create a second confession file at the same time, a fake confession file, and for you to ensure that both the real confession file (which you will then send to me) and the fake confession file both have the same hash (ie the last few digits of their SHA256 hashes are the same).

The contents of the real and fake confessions are below.

> This is the secret confession of Richard Buckland
> to be revealed by anonymous email if I should
> mysteriously vanish. I have left the last few hex
> digits of the SHA256 hash of this message with my
> trusted solicitor, Dennis Denuto, which will verify
> that this is indeed my intended and unaltered
> confession written by me Richard Buckland.
> 
> Dennis has not seen this confession he has only seen
> the last few digits of the hash. I have also sent copies
> of the last few digits to my bank manager and to my priest
> Father Brown.
> 
> On the 10th of February I saw Mark Zukerberg peeping
> through my window and recording my private and personal
> conversation with my friend.
> 
> I confronted him and he was very embarrassed. He
> promised to pay me $1 million a year if I would stay
> silent and not tell anyone I had seen him do this. I
> agreed but now I worry that it would be cheaper for him
> to make me vanish than to keep paying me.

And 

> This is the secret confession of Richard Buckland
> to be revealed by anonymous email if I should
> mysteriously vanish. I have left the last few hex
> digits of the SHA256 hash of this message with my
> trusted solicitor, Dennis Denuto, which will verify
> that this is indeed my intended and unaltered
> confession written by me Richard Buckland.
> 
> Dennis has not seen this confession he has only seen
> the last few digits of the hash. I have also sent copies
> of the last few digits to my bank manager and to my priest
> Father Brown.
> 
> On the 10th of February I saw Mark Zukerberg near my
> house and we struck up a conversation. He explained all
> the things he was doing to ensure that Facebook respects
> privacy - both of its users and of others. It was very
> impressive.
> 
> I feel awful that I have been criticising Facebook publicly
> for so long. I apologised to him in our conversation and
> now I want to confess to the world that actually Facebook
> has more than enough privacy features, and that the reason
> I spend so much time criticising Facebook is that I am
> envious of Mark and wish I was a clever and smart and wise
> as he is. I feel so bad for having been so mean to him for
> so many years that I am considering retreating to the outback.
> I may well cut off all contact with the world and live as a
> hermit from now on. So do not worry if I vanish it is just
> that I feel so guilty that I have been so unfair to Facebook.


Your first attempts at creating the ASCII files are below.  The last 2 digits of the sha256 for them are

Real: ...8d
Fake: ...11

TXT
confession_real.txt
TXT
confession_fake.txt
 Download confession_real.txt (0.9 KiB)


## What you are to do
*If you are doing this by hand - just make the last 2 hex digits of the files match.  If you are scripting or coding a solution your challenge is to see how many digits you can get to match.* 

Create two files (one real confession, one fake), each of which looks like the provided confessions, but so that the SHA256 hashes of each file have the same last two digits (or more digits if you are using coding).  They should differ from the provided files only in the presence or absence of a space character at the end of each line (the provided files have no space character at the end of any line).
Log your method and how you go about finding the files, plus attach the two files and their hashes.
Post a summary comment below, including the matching digits of your two confessions.  (Copy it into your logbook too)
If you are stuck at any time check out the page of [resources and hints](https://www.openlearning.com/unswcyber/courses/security-engineering-23t3/activities/birthday/hints/?cl=1)

## Resources and hints (not yet read, here for reference)
How to alter text files so they look the same, but are actually different (ie so they generate different SHA256 hashes but look the same to the eye?)

The confession files have more than 10 lines each.  One simple method is as follows:

If a line ends in a space call it 1, if a line has no space call it 0.  Count up in binary to generate different combinations of spaces and no spaces.  That will generate 2ˆ10 combinations (just using the first 10 lines).

eg if lines 1, 3, and 5 have a space at the end, and all the other lines don't, then that is variant number 0000010101

 

How to compute SHA256 hashes fast?

Coding/Scripting:

If you are a programmer and want to code it calling a crypto library (or just want to script openssl) that's fine.  In that case see how many digits of the two SHA256 hashes you can get to match.  The tips below are for everyone else.

Manually:

You can do it manually on a website like

https://gchq.github.io/CyberChef/#recipe=SHA2('256',64,160)
This site computes SHA2656 hashes for files, AND
you can also enter and hash text directly, which is convenient for manually trying lots of variants fast.
 

 

Text File format

Windows sometimes uses two special characters CR-LF to mark the end of lines of text files.  Linus and mac tend to just use LF.   (LF is the ASCII code for Line Feed it is code OA in hex, CR is the ASCII code for Carriage Return, it is 0D in hex).

All the interactive online SHA256 generators that I've tested so far (including the one listed above which I recommend as being quite useful) assume that when you are typing text into the web page and press enter to make a new line, they assume that the file being hashed has a LF inserted at that spot.  

So if you are a windows user who is generating and testing the confession variants using an interactive online SHA256 generator - then when you have found matching confessions make sure you save them using a text editor which uses linux/unix style end of line characters, not windows CR-LF pairs, or your file's SHA256 hash won't match what you saw in the interactive window.

Also make sure your text file, and your testing text, has a new line at the end of the last line.

If you want to see what is going on view your text files using a hex editor.  it should end in a solo LF (ie 0A) , and not a CR-LF pair (ie 0D0A).  

Below are two sample files just containing the word "testing" you can down load as tests.  One terminates the line using LF, one uses CR-LF.  You can inspect them using a hex editor to see the difference.  Their corresponding SHA256 hashes are also shown.  Type testing into an online SHA256 generator and check that it generates the correct hash.  Then create a text file yourself containing just the word "testing" (without the quotes) and terminating with a LF and  SHA256 hash that to test that you are creating text files correctly.

testing-lf.txt: (unix/linux/mac format) - SHA256 hash ends in "...c2"
testing-crlf.txt: (windows format) - SHA256 hash ends in "...2b"
