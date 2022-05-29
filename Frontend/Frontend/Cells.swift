//
//  courseTableCell.swift
//  Frontend
//
//  Created by Joel Valerio on 5/1/22.
//


import Foundation
import UIKit

class courseTableCell: UITableViewCell {
    
    var courseLabel = UILabel()

    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        contentView.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        contentView.layer.cornerRadius = 12.0
        courseLabel.font = .systemFont(ofSize: 14)
        courseLabel.textColor = .black
        courseLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(courseLabel)
        
        setUpConstraints()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()

        contentView.frame = contentView.frame.inset(by: UIEdgeInsets(top: 5, left: 5, bottom: 5, right: 5))
    }
    
    func configure(course: Course){
        courseLabel.text = course.code
    }
    
    
    func setUpConstraints(){
        let padding: CGFloat = 15
        
        NSLayoutConstraint.activate([courseLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: padding), courseLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 0.5 * padding)])
    }
    
    
}

class TimeTableCell: UITableViewCell {
    
    var timeLabel = UILabel()

    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        contentView.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        contentView.layer.cornerRadius = 12.0
        timeLabel.font = .systemFont(ofSize: 14)
        timeLabel.textColor = .black
        timeLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(timeLabel)
        
        setUpConstraints()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()

        contentView.frame = contentView.frame.inset(by: UIEdgeInsets(top: 5, left: 5, bottom: 5, right: 5))
    }
    
    func configure(time: String){
        timeLabel.text = time
    }
    
    
    func setUpConstraints(){
        let padding: CGFloat = 15
        
        NSLayoutConstraint.activate([timeLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: padding), timeLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 0.5 * padding)])
    }
    
    
}

class SearchCell: UITableViewCell {
    
    var courseLabel = UILabel()

    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        contentView.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        contentView.layer.cornerRadius = 12.0
        
        courseLabel.font = .systemFont(ofSize: 14)
        courseLabel.textColor = .black
        courseLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(courseLabel)
        
        setUpConstraints()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func configure(course: String){
        courseLabel.text = course
    }
    
    
    func setUpConstraints(){
        let padding: CGFloat = 15
        
        NSLayoutConstraint.activate([courseLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: padding), courseLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 0.5 * padding)])
    }
}

class TutorCell: UITableViewCell {
    
    var image = UIImageView()
    var name = UILabel()
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        image.layer.cornerRadius = 100.0
        image.contentMode = .scaleAspectFit
        image.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(image)
        
        name.font = .systemFont(ofSize: 18)
        name.textColor = .black
        name.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(name)
        
        setUpConstraints()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    func configure(user: User) {
        self.image.image = UIImage(named: user.profile_pic)
        self.name.text = user.name
    }
    
    func setUpConstraints() {
        NSLayoutConstraint.activate([image.topAnchor.constraint(equalTo: contentView.topAnchor), image.bottomAnchor.constraint(equalTo: contentView.bottomAnchor), image.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 20), image.trailingAnchor.constraint(equalTo: image.leadingAnchor, constant: 40)])
        
        NSLayoutConstraint.activate([name.leadingAnchor.constraint(equalTo: image.trailingAnchor, constant: 20), name.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 10), name.bottomAnchor.constraint(equalTo: name.topAnchor, constant: 40), name.trailingAnchor.constraint(equalTo: contentView.trailingAnchor)])
    }
}
