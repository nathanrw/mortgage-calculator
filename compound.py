#!/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import itertools
import math


def pmt(principal, monthly_interest_rate, number_of_months):
    pv = principal
    i = monthly_interest_rate
    n = number_of_months
    return pv * (i / (1 - math.pow(1 + i, -n)))


class Writer(object):

    def __init__(self):
        self.property_details = None
        self.mortgage_details = None
        self.rows = None

    def begin_document(self):
        pass

    def end_document(self):
        pass

    def begin_property(self, price, service_charge):
        assert self.property_details is None
        self.property_details = {
            "price": price,
            "service_charge": service_charge
        }

    def end_property(self):
        assert self.property_details is not None
        self.property_details = None

    def begin_mortgage(self, deposit, term):
        assert self.property_details is not None
        assert self.mortgage_details is None
        price = self.property_details["price"]
        deposit_percent = (deposit / float(price)) * 100
        self.mortgage_details = {
            "deposit": deposit,
            "deposit_percent": deposit_percent,
            "term": term
        }

    def end_mortgage(self):
        assert self.mortgage_details is not None
        self.mortgage_details = None

    def begin_rows(self):
        assert self.property_details is not None
        assert self.mortgage_details is not None
        assert self.rows is None
        self.rows = []

    def add_row(self, rate):
        assert self.rows is not None
        price = self.property_details["price"]
        term = self.mortgage_details["term"]
        mortgage_pcm = pmt(price, rate/(100*12.0), term*12)
        service_charge = self.property_details["service_charge"]
        self.rows.append({
           "rate": rate,
           "mortgage_pcm": mortgage_pcm,
           "mortgage_cost": mortgage_pcm*term*12,
           "cost_pcm": mortgage_pcm + service_charge / 12.0
        })

    def end_rows(self):
        assert self.rows is not None
        self.rows = None


class PrintWriter(Writer):

    def begin_property(self, price, service_charge):
        Writer.begin_property(self, price, service_charge)
        price = self.property_details["price"]
        service_charge = self.property_details["service_charge"]
        print("Affordability for property priced at £%s with £%s annual service charge." % (price, service_charge))

    def end_property(self):
        print()
        Writer.end_property(self)

    def begin_mortgage(self, deposit, term):
        Writer.begin_mortgage(self, deposit, term)
        deposit_percent = self.mortgage_details["deposit_percent"]
        print("  With %.0f%% deposit of £%s and term of %s years:" % (deposit_percent, deposit, term))

    def end_mortgage(self):
        Writer.end_mortgage(self)

    def begin_rows(self):
        Writer.begin_rows(self)

    def end_rows(self):
        print("    Total mortgage cost: ", end="")
        for row in self.rows:
            print("£%.2f [%s%%] " % (row["mortgage_cost"], row["rate"]), end="")
        print()
        print("    Monthly mortgage cost: ", end="")
        for row in self.rows:
            print("£%.2f [%s%%] " % (row["mortgage_pcm"], row["rate"]), end="")
        print()
        print("    Monthly cost: ", end="")
        for row in self.rows:
            print("£%.2f [%s%%] " % (row["cost_pcm"], row["rate"]), end="")
        print()
        Writer.end_rows(self)


class HtmlWriter(Writer):

    def begin_document(self):
        pass

    def end_document(self):
        pass

    def begin_property(self, price, service_charge):
        Writer.begin_property(self, price, service_charge)
        price = self.property_details["price"]
        service_charge = self.property_details["service_charge"]
        print("<h1>Affordability for property priced at £%s with £%s annual service charge.</h1>" % (price, service_charge))

    def end_property(self):
        print()
        Writer.end_property(self)

    def begin_mortgage(self, deposit, term):
        Writer.begin_mortgage(self, deposit, term)
        deposit_percent = self.mortgage_details["deposit_percent"]
        print("<h2>With %.0f%% deposit of £%s and term of %s years</h2>" % (deposit_percent, deposit, term))

    def end_mortgage(self):
        Writer.end_mortgage(self)

    def begin_rows(self):
        Writer.begin_rows(self)

    def end_rows(self):
        print("<table>")
        print("<tr>")
        print("<td></td>")
        for row in self.rows:
            print("<td>%s%%</td>" % row["rate"])
        print("</tr>")
        print("<tr>")
        print("<td>Total mortgage cost</td>")
        for row in self.rows:
            print("<td>£%.2f</td>" % row["mortgage_cost"])
        print("</tr>")
        print("<tr>")
        print("<td>Monthly mortgage cost</td>")
        for row in self.rows:
            print("<td>£%.2f</td>" % row["mortgage_pcm"])
        print("</tr>")
        print("<tr>")
        print("<td>Monthly cost</td>")
        for row in self.rows:
            print("<td>£%.2f</td>" % row["cost_pcm"])
        print("</tr>")
        print("</table>")
        Writer.end_rows(self)


def main():
    prices = [ 135000, 180000, 200000, 220000 ]
    service_charges = [ 0, 2000, 3000 ] # per year
    deposits = [ 30000, 40000 ]
    interest_rates = [ 2.0, 4.0, 10.0 ]
    terms = [ 25, 30, 35 ]

    writer = HtmlWriter()
    writer.begin_document()
    for price in prices:
        for service_charge in service_charges:
            writer.begin_property(price, service_charge)
            for deposit in deposits:
                for term in terms:
                    writer.begin_mortgage(deposit, term)
                    writer.begin_rows()
                    for rate in interest_rates:
                        writer.add_row(rate)
                    writer.end_rows()
                    writer.end_mortgage()
            writer.end_property()
    writer.end_document()


if __name__ == '__main__':
    main()
