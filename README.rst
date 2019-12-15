######################################################
mtg-dataset - yet another Magic: the Gathering dataset
######################################################

I guess that I'm throwing my head into the ring and making another Magic: the
Gathering dataset.

**************************
Why another Magic dataset?
**************************

#.  I'm tired of wasting CPU cycles and bandwidth loading gigantic JSON files
    when other file formats can provide the same data in smaller formats with
    substantially faster deserialization.
#.  I don't entirely agree with the schemas or data organization choices made
    by any of the other dataset maintainers.

************
Requirements
************

-   make
-   jq
-   Python 3.7+
-   Java JDK compatible with Spark

************
Installation
************

#.  Clone the repo
#.  `pip install -r requirements.txt`

********************
Building the dataset
********************

.. code:: bash

    make
