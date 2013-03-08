class Post < ActiveRecord::Base
  attr_accessible :text, :user_id
  belongs_to :user
  has_many :comments
end
