//
//  HomeController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/1/22.
//

import Foundation
import UIKit
import Alamofire

/** To-Do to integrate networking:
 1 . getAllUserCourses to fill out classes that user is tutoring in
 2. getAllNotifications to fill out notification table
 3. Post request for notifications when user request help
 3. Implement the search bar along with collectionview for displaying available tutors ( Will need a getByCourse
 method for users)
 4. Post request to add to the tutoring array
 5. Post request to add available times
 6. Delete request to delete availability
 7. Delete request to delete course
 8. Set up authentication and login screen
 9. Get request for getting the images of tutors ( If we need to drop the images idea then we can fill out the search results as a table rather than just displaying images of users)
 10. Put, Get, and Post Request for rates
 */

// If name equals "", then show persistent alert that asks for name

class ProfileController: UIViewController {
    
    var ownAccount = true
    var user: User!
    weak var userViewing: User?
    
    var profilePic = UIImageView()
    var name = UILabel()
    var email = UILabel()
    var tutoring = UITableView()
    var availability = UITableView()
    var tutorLabel = UILabel()
    var availabilityLabel = UILabel()
    var rateLabel = UILabel()
    let addCourseString = "+ Add a course to tutor in! "
    let addTimeString = "+ Add a new time!"
    let rateCash = UILabel()
    let rateField = UITextField()
    let rateTime = UILabel()
    let addRow = Course(code: "+ Add a course to tutor in! ", tutors: [], id: 1000000)
    var addTime: Availability!
    
    let requestHelp = UIButton()
    let requestSent = UILabel()
    
    let reuseID = "Courses"
    let reuseID2 = "Times"
    var padding = 20.0
    
    var courses : [Course] = []
    var times : [Availability] = []
    
    convenience init(ownAccount: Bool, user: User) {
        self.init()
        
        self.user = user
        self.ownAccount = ownAccount
    }
    
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        view.backgroundColor = .white
        
        
        profilePic.image = UIImage(named: "profile.png")
        profilePic.layer.cornerRadius = 100.0
        profilePic.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(profilePic)
        
        name.text = self.user.name
        name.font = .systemFont(ofSize: 18)
        name.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(name)
        
        email.text = self.user.email
        email.font = .systemFont(ofSize: 14)
        email.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(email)
        
        tutorLabel.text = "Tutor ✏️"
        tutorLabel.font = .systemFont(ofSize: 18)
        tutorLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(tutorLabel)
        
        tutoring.layer.cornerRadius = 14.0
        tutoring.dataSource = self
        tutoring.register(courseTableCell.self, forCellReuseIdentifier: reuseID)
        tutoring.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(tutoring)
        
        availabilityLabel.text = "Available Times ⏰"
        availabilityLabel.font = .systemFont(ofSize: 18)
        availabilityLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(availabilityLabel)
        
        rateLabel.text = "Rate 💵"
        rateLabel.font = .systemFont(ofSize: 18)
        rateLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(rateLabel)
        
        availability.layer.cornerRadius = 14.0
        availability.dataSource = self
        availability.register(TimeTableCell.self, forCellReuseIdentifier: reuseID2)
        availability.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(availability)
        
        rateCash.text = " $"
        rateCash.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        rateCash.font = .systemFont(ofSize: 18)
        rateCash.textAlignment = .center
        rateCash.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(rateCash)
        
        if self.user.rate != nil {
            rateField.text = self.user.rate
        } else {
            rateField.placeholder = "..."
        }
        
        rateField.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        rateTime.font = .systemFont(ofSize: 18)
        rateField.borderStyle = .none
        rateField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(rateField)
        
        rateTime.text = "/ hour"
        rateTime.font = .systemFont(ofSize: 18)
        rateTime.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        rateTime.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(rateTime)
        
        self.courses = self.user.teaching!
        self.times = self.user.availability
        
        if ownAccount {
            // MARK: Make users able to delete a course or availability
            tutoring.delegate = self
            availability.delegate = self
            rateField.delegate = self
            rateField.isUserInteractionEnabled = true
            
            self.courses.append(addRow)
            self.times.append(addTime)
            
        } else {
            
            requestHelp.setTitle(" Request Help! ", for: .normal)
            requestHelp.setTitleColor(.black, for: .normal)
            requestHelp.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
            requestHelp.layer.cornerRadius = 5.0
            requestHelp.addTarget(self, action: #selector(helpRequest), for: .touchUpInside)
            requestHelp.translatesAutoresizingMaskIntoConstraints = false
            view.addSubview(requestHelp)
            
            requestSent.text = ""
            requestSent.textAlignment = .center
            requestSent.font = .systemFont(ofSize: 18, weight: .bold)
            requestSent.translatesAutoresizingMaskIntoConstraints = false
            view.addSubview(requestSent)
            
            NSLayoutConstraint.activate([requestHelp.topAnchor.constraint(equalTo: rateField.bottomAnchor, constant: 2 * padding), requestHelp.bottomAnchor.constraint(equalTo: requestHelp.topAnchor, constant: 2 * padding), requestHelp.leadingAnchor.constraint(equalTo: rateField.leadingAnchor,constant: padding),requestHelp.trailingAnchor.constraint(equalTo: rateField.trailingAnchor, constant: -padding)])
            
            NSLayoutConstraint.activate([requestSent.topAnchor.constraint(equalTo: requestHelp.bottomAnchor, constant: padding), requestSent.bottomAnchor.constraint(equalTo: requestSent.topAnchor, constant: 2 * padding), requestSent.leadingAnchor.constraint(equalTo: requestHelp.leadingAnchor, constant: padding), requestSent.trailingAnchor.constraint(equalTo: requestHelp.trailingAnchor, constant: padding)])
            
        }
        
        tutoring.reloadData()
        
        setUpContraints()
    }
    
    func setUpContraints() {
        NSLayoutConstraint.activate([profilePic.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor), profilePic.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: 2 * padding)])
        
        NSLayoutConstraint.activate([name.topAnchor.constraint(equalTo: profilePic.topAnchor), name.leadingAnchor.constraint(equalTo: profilePic.trailingAnchor, constant: padding - 10), name.bottomAnchor.constraint(equalTo: name.topAnchor,constant: padding)])
        
        NSLayoutConstraint.activate([email.topAnchor.constraint(equalTo: name.bottomAnchor, constant: padding - 15), email.bottomAnchor.constraint(equalTo: email.topAnchor, constant: padding),email.leadingAnchor.constraint(equalTo: name.leadingAnchor)])
        
        NSLayoutConstraint.activate([tutorLabel.topAnchor.constraint(equalTo: email.bottomAnchor, constant: 2 * padding), tutorLabel.leadingAnchor.constraint(equalTo: profilePic.leadingAnchor), tutorLabel.bottomAnchor.constraint(equalTo: tutorLabel.topAnchor, constant: padding)])
        
        NSLayoutConstraint.activate([tutoring.topAnchor.constraint(equalTo: tutorLabel.bottomAnchor, constant: 5), tutoring.bottomAnchor.constraint(equalTo: tutoring.topAnchor, constant: 150),tutoring.leadingAnchor.constraint(equalTo: profilePic.leadingAnchor),tutoring.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding)])
        
        NSLayoutConstraint.activate([availabilityLabel.topAnchor.constraint(equalTo: tutoring.bottomAnchor, constant: padding), availabilityLabel.leadingAnchor.constraint(equalTo: tutorLabel.leadingAnchor),availabilityLabel.bottomAnchor.constraint(equalTo: availabilityLabel.topAnchor, constant: padding)])
        
        NSLayoutConstraint.activate([availability.topAnchor.constraint(equalTo: availabilityLabel.bottomAnchor, constant: 5),availability.bottomAnchor.constraint(equalTo: availability.topAnchor, constant: 80),availability.leadingAnchor.constraint(equalTo: tutoring.leadingAnchor),availability.trailingAnchor.constraint(equalTo: tutoring.trailingAnchor)])
        
        NSLayoutConstraint.activate([rateLabel.topAnchor.constraint(equalTo: availability.bottomAnchor, constant: padding), rateLabel.leadingAnchor.constraint(equalTo: availabilityLabel.leadingAnchor), rateLabel.bottomAnchor.constraint(equalTo: rateLabel.topAnchor, constant: padding)])
        
        NSLayoutConstraint.activate([rateCash.centerYAnchor.constraint(equalTo: rateField.centerYAnchor),rateCash.leadingAnchor.constraint(equalTo: tutoring.leadingAnchor), rateCash.trailingAnchor.constraint(equalTo: rateCash.leadingAnchor, constant: 20), rateCash.topAnchor.constraint(equalTo: rateField.topAnchor), rateCash.bottomAnchor.constraint(equalTo: rateField.bottomAnchor)])
        
        NSLayoutConstraint.activate([rateField.topAnchor.constraint(equalTo: rateLabel.bottomAnchor, constant: padding),rateField.bottomAnchor.constraint(equalTo: rateField.topAnchor, constant: 2 * padding), rateField.leadingAnchor.constraint(equalTo: rateCash.trailingAnchor), rateField.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -80)])
        
        NSLayoutConstraint.activate([rateTime.centerYAnchor.constraint(equalTo: rateField.centerYAnchor), rateTime.leadingAnchor.constraint(equalTo: rateField.trailingAnchor), rateTime.trailingAnchor.constraint(equalTo: tutoring.trailingAnchor), rateTime.topAnchor.constraint(equalTo: rateField.topAnchor),rateTime.bottomAnchor.constraint(equalTo: rateField.bottomAnchor)])

    }
    
    func showAlert() {
        let alert = UIAlertController(title: "Invalid rate", message: "Must input a number", preferredStyle: .alert)
        
        let invalidate = { self.rateField.invalidate(placeholder: "15.00") }
        alert.addAction(UIAlertAction(title: "Ok", style: .cancel) { _ in invalidate()})
        
        present(alert, animated: true,completion: nil)
    }
    
    @objc func helpRequest() {
        
        NetworkManager.createNotification(senderID: self.userViewing!.id, receiverID: self.user.id) { _ in}
        presentingViewController?.dismiss(animated: true)
        dismiss(animated: true)
    }
    
}

extension ProfileController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if tableView == tutoring {
            return courses.count
        } else {
            return times.count
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        if tableView == tutoring {
            if let cell = tableView.dequeueReusableCell(withIdentifier: reuseID, for: indexPath) as? courseTableCell {
                let courses = courses[indexPath.row]
                cell.configure(course: courses)
                cell.selectionStyle = .none
                return cell
            }
            else {
                return UITableViewCell()
            }
            
        } else {
            if let cell = tableView.dequeueReusableCell(withIdentifier: reuseID2, for: indexPath) as? TimeTableCell {
                let time = times[indexPath.row]
                cell.configure(time: time.time)
                cell.selectionStyle = .none
                return cell
            }
            else {
                return UITableViewCell()
            }
        }
        
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 40
    }
}

extension ProfileController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableView == tutoring {
            
            let selectedRow = courses[indexPath.row]
            if selectedRow.code == addCourseString {
                presentController()
            } else {
                NetworkManager.dropTutor(courseID: selectedRow.id, UserID: user.id) { User in
                    self.courses = self.user.teaching!
                    self.courses.append(self.addRow)
                    self.tutoring.reloadData()
                }
            }
        } else {
            
            let selectedRow = times[indexPath.row]
            if selectedRow.time == addTimeString {
                presentController2()
            } else {
                NetworkManager.deleteAvailability(userID: self.user.id, availID: selectedRow.id) { Availability in
                    
                    var index = 0
                    while index < self.times.count {
                        if Availability.id == self.times[index].id {
                            self.times.remove(at: index)
                            index += 1
                        }
                        index += 1
                    
                    }
                    self.times = self.user.availability
                    self.times.append(self.addTime)
                    self.availability.reloadData()
                }
            }
        }
    }
    
    @objc func presentController() {
        let vc = CourseController(num: 1, user: user)
        vc.parentController = self
        navigationController?.pushViewController(vc, animated: true)
    }
    @objc func presentController2() {
        let vc = addTimeController()
        vc.parentController = self
        vc.user = user
        navigationController?.pushViewController(vc, animated: true)
    }
}

extension ProfileController: UITextFieldDelegate {
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        rateField.resignFirstResponder()
        return true
    }
    
    func textFieldShouldEndEditing(_ textField: UITextField) -> Bool {
        if let text = rateField.text {
            if let double = Double(text) {
                let rate = String(double)
                let userID = String(self.user.id)
                NetworkManager.updateRate(userID: userID, rate: rate) { _ in}
                return true
            }
            showAlert()
            return false
        }
        showAlert()
        return false
    }
}

extension UITextField {
    func invalidate(placeholder: String) {
        attributedPlaceholder = NSAttributedString(
            string: placeholder,
            attributes: [.foregroundColor : UIColor.systemRed.withAlphaComponent(0.55) ]
        )
    }
}


