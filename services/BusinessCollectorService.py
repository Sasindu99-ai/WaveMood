import threading
from queue import Queue

from sqlalchemy import Column, String, Integer, Float

from services import GMapService
from vvecon.qt.db import Database
from vvecon.qt.logger import logger
from vvecon.qt.thread import threadPool


class BusinessCollectorService:
    def __init__(self, search_text, lat_min, lat_max, lng_min, lng_max, step):
        self.search_text = search_text
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lng_min = lng_min
        self.lng_max = lng_max
        self.step = step
        self.service = GMapService()
        self.db = Database('businesses.db')  # Use the existing Database class

        class Business(self.db.Model):
            __tablename__ = 'businesses'

            placeId = Column(String)
            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String)
            address = Column(String)
            lat = Column(Float)
            lng = Column(Float)
            rating = Column(Float)
            user_ratings_total = Column(Integer)

        self.db.create_all()  # Ensure the database schema is created
        self.business_model = Business

        # Initialize a queue for database operations
        self.queue = Queue()
        self.queue_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.queue_thread.start()

    def _process_queue(self):
        """Process the queue and commit database operations."""
        while True:
            business_entry = self.queue.get()
            try:
                self.db.session.add(business_entry)
                self.db.session.commit()
            except Exception as e:
                logger.error(f"Error committing to the database: {e}")
            finally:
                self.queue.task_done()

    def process_square(self, square):
        lat1, lng1, lat2, lng2 = square
        center_lat = (lat1 + lat2) / 2
        center_lng = (lng1 + lng2) / 2
        location = f"{center_lat},{center_lng}"
        businesses = self.service.searchBusinesses(location, radius=1000, query=self.search_text)
        for business in businesses:
            try:
                place_id = business.get('place_id')
                # Check if the place already exists in the database
                exists = self.db.session.query(self.business_model).filter_by(placeId=place_id).first()
                if exists:
                    continue

                lat = float(business['geometry']['location']['lat'])
                lng = float(business['geometry']['location']['lng'])
                rating = business.get('rating', 0)
                if isinstance(rating, str) and rating.isdigit():
                    rating = float(rating)
                elif isinstance(rating, (int, float)):
                    rating = float(rating)
                else:
                    rating = 0.0
                user_ratings_total = int(business.get('user_ratings_total', 0))

                business_entry = self.business_model(
                    placeId=place_id,
                    name=business.get('name'),
                    address=business.get('formatted_address'),
                    lat=lat,
                    lng=lng,
                    rating=rating,
                    user_ratings_total=user_ratings_total
                )
                # Add the business entry to the queue
                self.queue.put(business_entry)
            except (ValueError, TypeError, KeyError) as e:
                logger.error(f"Error processing business data: {e}")
                logger.debug(f"Problematic business entry: {business}")

    def run(self):
        squares = self.service.generate_squares(self.lat_min, self.lat_max, self.lng_min, self.lng_max, self.step)
        for square in squares:
            threadPool.start(self.process_square, square)