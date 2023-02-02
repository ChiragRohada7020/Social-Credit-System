from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import abort, redirect, url_for,session
import pymongo
from flask_mysqldb import MySQL
import mysql.connector
import l


def update():
    
    
    # Connect to the database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="social_credit_system"
    )
    cursor = cnx.cursor()

    query = "SELECT Source FROM cctv_footage "
    cursor.execute(query)
    x=cursor.fetchall()
    print(x)
    def convert_range(original_value):
        original_min = 0
        original_max = 300
        new_min = 500
        new_max = 2500
        new_value = (((original_value - original_min) * (new_max -
                    new_min)) / (original_max - original_min)) + new_min
        return new_value


    # Retrieve all the individuals in the Social_Credit_Score table
    query = "SELECT Individual_ID FROM social_credit_score"
    cursor.execute(query)
    individual_ids = cursor.fetchall()

    for individual_id in individual_ids:
        # Retrieve an individual's credit score from the Credit_Score table
        query = "SELECT Credit_Score FROM credit_score WHERE Individual_ID = %s"
        cursor.execute(query, (individual_id[0],))
        credit_score = int(cursor.fetchone()[0]/9)
        print(credit_score)
        query = "SELECT Tax FROM credit_score WHERE Individual_ID = %s"
        cursor.execute(query, (individual_id[0],))
        tax_paid = int(cursor.fetchone()[0])
        if tax_paid > 14000:
            credit_score += 100
        elif tax_paid > 0:
            credit_score += 50

        # Retrieve an individual's criminal records score from the Criminal_Records table
        query = "SELECT SUM(Crime_Score) FROM criminal_records WHERE Individual_ID = %s"
        cursor.execute(query, (individual_id[0],))
        criminal_score = cursor.fetchone()[0]

        # Retrieve an individual's behaviour score from the Behaviour_Records table
        query = "SELECT SUM(Behaviour_Score) FROM behaviour_records WHERE Individual_ID = %s"
        cursor.execute(query, (individual_id[0],))
        behaviour_score = cursor.fetchone()[0]

        query = "SELECT Relationship FROM family_details WHERE Individual_ID = %s AND Relationship = 'child'"
        cursor.execute(query, (individual_id[0],))
        relationship = cursor.fetchone()
        family_score = 0
        # Check if the individual has a spouse
        print(relationship)
        if relationship:
            family_score += 40

        query = "SELECT Relationship FROM family_details WHERE Individual_ID = %s AND Relationship = 'spouse'"
        cursor.execute(query, (individual_id[0],))
        relationship = cursor.fetchone()
        # Check if the individual has a spouse
        if relationship:
            family_score += 25

        query = "SELECT Relationship FROM family_details WHERE Individual_ID = %s AND Relationship = 'parents'"
        cursor.execute(query, (individual_id[0],))
        relationship = cursor.fetchone()
        # Check if the individual has a spouse
        if relationship:
            family_score += 20

        query = "SELECT Relationship FROM family_details WHERE Individual_ID = %s AND Relationship = 'others'"
        cursor.execute(query, (individual_id[0],))
        relationship = cursor.fetchone()
        # Check if the individual has a spouse
        if relationship:
            family_score += 15

        social_credit_score = credit_score + \
            criminal_score + behaviour_score + family_score
        social_credit_score = convert_range(social_credit_score)
        # Update the Social_Credit_Score table with the new score
        query = "UPDATE social_credit_score SET Social_Credit_Score = %s WHERE Individual_ID = %s"
        cursor.execute(query, (social_credit_score, individual_id[0]))
        cnx.commit()

    # Close the cursor and the connection
    cursor.close()
    cnx.close()


update()

