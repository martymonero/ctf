# Misc/Git

This was by far the easiest challenge of this event, but a good warm up nonetheless.

The task was to recover a file from a git repository.

You were given a zip archive that contains a local git repository. Inspecting the folder shows only a HelloWorld.txt file. No flag in sight.

We can assume that the flag is hidden in one of the earlier commits.

As someone who always works on his own git repository and commits directly to the master branch I wasn't really a git expert at this point. 

![Git Meme](https://d3suqxyr95ccqd.cloudfront.net/sites/default/files/styles/image_600_width/public/secondary_images/images_and_text/gitflow-no-commit-to-master.jpg?itok=ucTkD0WY
)

But as you know hacking is about being able to research new topics on the fly.

A couple google queries later I found two commands that revealed the necessary information. Key was to include the reflogs.

```
git log -g
```
or even better

```
git reflog show HEAD
```

The latter command gave this nice list and revealed a coommit:

```
22d3349 HEAD@{0}: checkout: moving from develop to master
22d3349 HEAD@{1}: rebase -i (finish): returning to refs/heads/develop
22d3349 HEAD@{2}: rebase -i (start): checkout 22d3349
f671986 HEAD@{3}: checkout: moving from master to develop
22d3349 HEAD@{4}: checkout: moving from develop to master
f671986 HEAD@{5}: checkout: moving from master to develop
22d3349 HEAD@{6}: checkout: moving from rctf to master
f671986 HEAD@{7}: commit: Revert
f4d0f6d HEAD@{8}: commit: Flag
22d3349 HEAD@{9}: checkout: moving from master to rctf
22d3349 HEAD@{10}: commit (initial): Initial Commit
```

Now I only needed to to:

```
git checkout -b flag-reveal f4d0f6d
```

A new file magically appeared called flag.txt with the fitting content :

```
RCTF{gIt_BranCh_aNd_l0g}
```

