class ListingService:
    @staticmethod
    def get_all_listings():
        return Listing.query.all()
    
    @staticmethod
    def get_listing_by_id(listing_id):
        return Listing.query.get(listing_id)
    
    @staticmethod
    def create_listing(data):
        new_listing = Listing(**data)
        return new_listing
    
    @staticmethod
    def update_listing(listing_id, data):
        listing = Listing.query.get(listing_id)
        if not listing:
            return None
        
        for key, value in data.items():
            setattr(listing, key, value)
            return listing
        
        @staticmethod
        def delete_listing(listing_id):
            listing = Listing.query.get(listing_id)
            if not listing:
                return None