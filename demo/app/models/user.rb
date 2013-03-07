class User < ActiveRecord::Base
  attr_accessible :email, :name
  has_many :posts
  has_many :comments
end
