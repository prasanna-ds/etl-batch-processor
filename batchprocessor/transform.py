
import pandas as pd
from .log import getLogger

LOG = getLogger(__name__)

class Transform:
    def __init__(self, events):
        self.events = events

    def transform(self):

        if not self.events:
            LOG.warning("Ignoring empty batch")
            return None

        df = pd.DataFrame.from_dict(pd.io.json.json_normalize(self.events))
        
        # creating fact - flats
        fact_flats = df[['data.id',
                         'data.publishDate',
                         'data.realEstate_apartmentType',
                         'data.realEstate_assistedLiving',
                         'data.realEstate_balcony',
                         'data.realEstate_baseRent',
                         'data.realEstate_builtInKitchen',
                         'data.realEstate_calculatedTotalRent',
                         'data.realEstate_calculatedTotalRentScope',
                         'data.realEstate_cellar',
                         'data.realEstate_certificateOfEligibilityNeeded',
                         'data.realEstate_condition',
                         'data.realEstate_constructionYear',
                         'data.realEstate_deposit',
                         'data.realEstate_descriptionNote',
                         'data.realEstate_floor',
                         'data.realEstate_freeFrom',
                         'data.realEstate_garden',
                         'data.realEstate_guestToilet',
                         'data.realEstate_handicappedAccessible',
                         'data.realEstate_heatingCosts',
                         'data.realEstate_heatingCostsInServiceCharge',
                         'data.realEstate_heatingType',
                         'data.realEstate_interiorQuality',
                         'data.realEstate_lastModificationDate',
                         'data.realEstate_lastRefurbishment',
                         'data.realEstate_lift',
                         'data.realEstate_livingSpace',
                         'data.realEstate_numberOfFloors',
                         'data.realEstate_numberOfRooms',
                         'data.realEstate_petsAllowed',
                         'data.realEstate_serviceCharge',
                         'data.realEstate_state',
                         'data.realEstate_totalRent',
                         ]]
        fact_flats.name = 'flats'                 

        # Creating dimension - address
        dim_address = df[[
            'data.id',
            'data.realEstate_address_city',
            'data.realEstate_address_geoHierarchy_city_name',
            'data.realEstate_address_geoHierarchy_country_name',
            'data.realEstate_address_geoHierarchy_quarter_name',
            'data.realEstate_address_geoHierarchy_region_name',
            'data.realEstate_address_postcode',
        ]]
        dim_address.name = 'address'
        
        # Creating dimension - agency
        dim_agency = df[[
            'data.id',
            'data.contactDetails_company',
            'data.contactDetails_email',
            'data.contactDetails_firstname',
            'data.contactDetails_lastname',
            'data.contactDetails_cellPhoneNumber',
            'data.contactDetails_cellPhoneNumberAreaCode',
            'data.contactDetails_cellPhoneNumberCountryCode',
            'data.contactDetails_phoneNumber',
		    'data.contactDetails_phoneNumberAreaCode',
		    'data.contactDetails_phoneNumberCountryCode',
        ]]
        dim_agency.name = 'agency'
     
        return [fact_flats, dim_address, dim_agency]
