# -*- coding: utf-8 -*-

'''
We are writing a script that will be used to analyze behavioral data in a 2AC task

'''


def test_mouse_summary_table(bdata, subject, sessions): 
    
    """
    Args:
        bdata () : 
        subject (str) : The name of the mouse.
        session (list of str): A list of all the sessions saved for the animal.

    Return: 
        mouse_table (pandas.DataFrame): A table which contains summary information (hits, misses, errors, percent correct, etc.) about each session for one mouse.  
    """
    
def test_stage3_percent_correct(mouse_table):
    
    """
    Args: 
        mouse_table (pandas.DataFrame): A table which contains summary information (hits, misses, errors, percent correct, etc.) about each session for one mouse.  

    Return:
        stage3_percent_correct (plt.scatter): A scatter plot which takes the percent correct from the mouse table and plots it across sessions. 
    """

def test_hits_per_session(mouse_table):
    
    """
    Args: 
        mouse_table (pandas.DataFrame): A table which contains summary information (hits, misses, errors, percent correct, etc.) about each session for one mouse.  

    Return:
        hits_per_session (plt.scatter): A scatter plot which takes the hits on the left and right side from the mouse table and plots it across sessions. 
    """


