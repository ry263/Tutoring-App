//
//  addCourseController.swift
//  Frontend
//
//  Created by Joel Valerio on 5/2/22.
//

import Foundation
import UIKit

class addTimeController: UIViewController {
    
    weak var parentController: ProfileController?
    weak var user: User!
    var datePicker = UIDatePicker()
    var label = UILabel()
    var dismissLabel = UILabel()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        label.text = "New Time ⏰"
        label.font = .systemFont(ofSize: 18)
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        
        datePicker.datePickerMode = .dateAndTime
        datePicker.minimumDate = Date()
        datePicker.minuteInterval = 30
        datePicker.addTarget(self, action: #selector(getSelected), for: .editingDidEnd)
        datePicker.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(datePicker)
        
        dismissLabel.text = ""
        dismissLabel.font = .systemFont(ofSize: 18)
        dismissLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(dismissLabel)
        
        setUpConstraints()
    }
    func setUpConstraints() {
        NSLayoutConstraint.activate([label.centerYAnchor.constraint(equalTo: view.safeAreaLayoutGuide.centerYAnchor,constant: -80), label.centerXAnchor.constraint(equalTo: view.centerXAnchor)])
        
        NSLayoutConstraint.activate([datePicker.topAnchor.constraint(equalTo: label.bottomAnchor, constant: 10),datePicker.centerXAnchor.constraint(equalTo: view.centerXAnchor)])
        
        NSLayoutConstraint.activate([dismissLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor), dismissLabel.centerYAnchor.constraint(equalTo: datePicker.centerYAnchor, constant: 40)])
    }
    @objc func getSelected() {
        let dateFormatter = DateFormatter()
        dateFormatter.dateStyle = DateFormatter.Style.short
        dateFormatter.timeStyle = DateFormatter.Style.short

        let strDate = dateFormatter.string(from: datePicker.date)
        
        NetworkManager.addAvailability(userID: user.id, time: strDate) { avail in
        }
        let finalAvail = Availability(time: strDate, userID: user.id, ID: 4)
        self.navigationController?.popViewController(animated: true)
        parentController!.times.insert(finalAvail, at: 0)
        parentController?.availability.reloadData()
    }
}
