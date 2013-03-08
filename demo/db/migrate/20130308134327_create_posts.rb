class CreatePosts < ActiveRecord::Migration
  def change
    create_table :posts do |t|
      t.string :post
      t.string :posted_by

      t.timestamps
    end
  end
end
