# Copyright (c) 2015 Huawei Technologies Co., Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
SQLAlchemy models for cinder data.
"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from oslo_utils import timeutils
from sqlalchemy import Column, Integer, String, Text, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref, validates


CONF = cfg.CONF
BASE = declarative_base()

class TerracottaBase(models.TimestampMixin,
                 models.ModelBase):
    """Base class for TerracottaBase Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}

    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def delete(self, session):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = timeutils.utcnow()
        self.save(session=session)


class Host(BASE, TerracottaBase):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    host_name = Column(String(255))
    cpu_mhz = Column(String(255))
    cpu_cores = Column(String(255))
    cpu_vendor = Column(String(255))
    ram = Column(Integer, nullable=False, default=0)
    disabled = Column(Boolean, default=False)
    disabled_reason = Column(String(255))


class HostResourceUsage(BASE, TerracottaBase):
    __tablename__ = 'host_resource_usage'
    id = Column(Integer, primary_key=True)
    host_id = Column(String(255))
    cpu_mhz = Column(String(255))
    
    host = relationship(Host, backref="host_resource_usage",
                        foreign_keys=host_id,
                        primaryjoin='HostResourceUsage.host_id == Host.id')

class VM(BASE, TerracottaBase):
    __tablename__ = 'vms'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False)


class VmResourceUsage(BASE, TerracottaBase):
    __tablename__ = 'vm_resource_usage'
    id = Column(Integer, primary_key=True)
    vm_id = Column(String(255))
    cpu_mhz = Column(String(255))
    
    host = relationship(Host, backref="vm_resource_usage",
                        foreign_keys=vm_id,
                        primaryjoin='VmResourceUsage.vm_id == VM.id')
