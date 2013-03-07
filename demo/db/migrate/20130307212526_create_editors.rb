class CreateEditors < ActiveRecord::Migration
  def change
    create_table :editors do |t|
      t.string :name
      t.string :email
      t.string :password

      t.timestamps
    end
  end
end
