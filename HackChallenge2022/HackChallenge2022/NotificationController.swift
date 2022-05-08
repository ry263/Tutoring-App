//
//  NotificationController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/1/22.
//

import Foundation
import UIKit

class NotificationController: UIViewController {
    
    weak var user: User!
    var label = UILabel()
    var image = UIImageView()
    var notifs = UITableView()
    var notifArray : [Notification] = []
    var reuseID = "Notification"
    var notifiers : [User] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        view.backgroundColor = .white
        
        label.text = "Notifications"
        label.font = .systemFont(ofSize: 25, weight: .bold)
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        
        image.image = UIImage(named: "notif.png")
        image.contentMode = .scaleAspectFit
        image.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(image)
        
        notifs.layer.cornerRadius = 14.0
        notifs.translatesAutoresizingMaskIntoConstraints = false
        notifs.rowHeight = 40
        notifs.dataSource = self
        notifs.register(notifCell.self, forCellReuseIdentifier: reuseID)
        view.addSubview(notifs)
        
        NetworkManager.getUserNotifications(userID: user.id) { notif in
            self.notifArray = notif
        }
        for notification in self.notifArray {
            NetworkManager.getUserData(userID: notification.sender_id) { user in
                self.notifiers.append(user)
            }
        }
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        NSLayoutConstraint.activate([label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 25), label.bottomAnchor.constraint(equalTo: label.topAnchor, constant: 40), label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 40), label.trailingAnchor.constraint(equalTo: view.centerXAnchor,constant: 5)])
        
        NSLayoutConstraint.activate([image.topAnchor.constraint(equalTo: label.topAnchor),image.leadingAnchor.constraint(equalTo: label.trailingAnchor, constant: 10),image.bottomAnchor.constraint(equalTo: label.bottomAnchor),image.trailingAnchor.constraint(equalTo: image.leadingAnchor, constant: 40)])
        
        NSLayoutConstraint.activate([notifs.topAnchor.constraint(equalTo: image.bottomAnchor, constant: 20), notifs.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor), notifs.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20), notifs.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -20)])
    }
    
}

extension NotificationController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.notifiers.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if let cell = tableView.dequeueReusableCell(withIdentifier: reuseID, for: indexPath) as? notifCell {
            
            let notifier = self.notifiers[indexPath.row]
            cell.configure(user: notifier)
            cell.selectionStyle = .none
            return cell
        }
        else {
            return UITableViewCell()
        }
    }
}

class notifCell: UITableViewCell {
    
    var image = UIImageView()
    var label = UILabel()
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        
        label.font = .systemFont(ofSize: 18)
        label.textColor = .black
        label.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(label)
        
        image.contentMode = .scaleAspectFit
        image.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(image)
        
        setUpConstraints()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    func configure(user: User) {
        self.image.image = UIImage(named: "profile.png")
        self.label.text = "\(user.email) reached out"
    }
    
    func setUpConstraints() {
        NSLayoutConstraint.activate([image.centerYAnchor.constraint(equalTo: contentView.centerYAnchor), image.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 15), image.trailingAnchor.constraint(equalTo: image.leadingAnchor, constant: 20),image.topAnchor.constraint(equalTo: contentView.centerYAnchor, constant: -10), image.bottomAnchor.constraint(equalTo: contentView.centerYAnchor, constant: 10)])
        
        NSLayoutConstraint.activate([label.leadingAnchor.constraint(equalTo: image.trailingAnchor, constant: 15), label.centerYAnchor.constraint(equalTo: contentView.centerYAnchor)])
    }
    
}
