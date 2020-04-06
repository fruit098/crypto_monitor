from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Column, func, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from . import BASE_MODEL


class IP_Pool(BASE_MODEL):
    __tablename__ = "ip_pool"
    id = Column(BigInteger, primary_key=True)
    ip = Column(String, unique=True, index=True)
    last_seen = Column(DateTime(timezone=True))
    inserted = Column(DateTime(timezone=True), server_default=func.now())
    node_id = Column(BigInteger, ForeignKey("node.id"))
    node = relationship("Node", back_populates="ip_pool")


class Node(BASE_MODEL):
    __tablename__ = "node"
    id = Column(BigInteger, primary_key=True)
    user_agent = Column(String)
    active = Column(Boolean)
    highest_protocol = Column(String)
    services = Column(ARRAY(String))
    activities = relationship("NodeActivity")
    ip_pool = relationship("IP_Pool", uselist=False, back_populates="node")


class NodeActivity(BASE_MODEL):
    __tablename__ = "node_activity"
    id = Column(BigInteger, primary_key=True)
    start_of_activity = Column(DateTime(timezone=True))
    end_of_activity = Column(DateTime(timezone=True))
    node_id = Column(BigInteger, ForeignKey("node.id"))
