# tagspace

Web query classification using analysis of inter-article relationships in Wikipedia .

### Getting the code:

##### With git

``` 
$ git clone https://github.com/pranavrc/tagspace.git
$ cd tagspace/
$ . bin/activate
```

##### From ZIP

You can download the ZIP from [here](https://github.com/pranavrc/tagspace/archive/master.zip).

### Running the code:

To run the Python script from a terminal, we use the following command:

````
$ cd tagspace/
$ . bin/activate
$ python tagspace.py <article-name>
```

For instance, for the articles *Bacon* and *Networks*:

```
$ python tagspace.py bacon bacon -> Domestic_pig -> Even-toed_ungulate -> Ungulate -> Clade -> Organism -> Biology ->
Natural_science -> Science ->
Knowledge -> Awareness -> Conscious -> Quality_(philosophy) -> Philosophy

$ python tagspace.py networks networks -> Artificial_neural_network -> Machine_learning ->
Computer_science -> Science ->
Knowledge -> Awareness -> Conscious -> Quality_(philosophy) -> Philosophy

$ python main.py
Returns the final graph of tags, clustered into a dendrogram model. 
```
