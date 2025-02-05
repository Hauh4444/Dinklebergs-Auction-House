class ListingService:
    @staticmethod
    def get_all_listings():
        return Listing.query.all()