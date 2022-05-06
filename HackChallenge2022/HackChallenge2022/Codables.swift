//
//  User.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/1/22.
//

import Foundation
import UIKit

class User: Codable {
    var name: String
    var profile_pic: String
    var teaching: [Course]
    var availability: [Availability]
    var rate: String?
    var notifications: [Notification]
    var email: String
    var id: Int
    
    init(name: String, image: String, teaching: [Course], availability: [Availability], rate: String?, notifications:[Notification], email: String, ID: Int) {
        self.name = name
        self.profile_pic = image
        self.teaching = teaching
        self.availability = availability
        self.rate = rate
        self.notifications = notifications
        self.email = email
        self.id = ID
    }
}

class Course: Codable {
    var id: Int
    var code: String
    var tutors: [User]
    
    init(code: String,tutors: [User], id: Int) {
        self.code = code
        self.tutors = tutors
        self.id = id
    }
    
    func getCourseNumber() -> Int {
        if code == "+ Add a course to tutor in! " {
            return 10000
        }
        let text = self.code.suffix(4)
        return Int(text)!
    }
}

class Notification: Codable {
    var id: Int
    var sender_id: Int
    var receiver_id: Int
    var label: String
    var time: String
    
    init(image: String, label: String, senderID: Int, receiverID: Int, ID: Int, time: String) {
        self.label = label
        self.sender_id = senderID
        self.receiver_id = receiverID
        self.id = ID
        self.time = time
    }
}

class Availability: Codable {
    
    var time: String
    var userID: Int
    var id: Int
    
    init(time: String, userID: Int, ID: Int) {
        self.time = time
        self.userID = userID
        self.id = ID
    }
}


let MATH1120 = Course(code: "MATH 1120",tutors: [], id: 0)
let CS2110 = Course(code: "CS 2110",tutors:  [], id: 1)
let CS2800 = Course(code: "CS 2800", tutors: [], id: 2)
let INFO3300 = Course(code: "INFO 3300", tutors: [], id: 3)

let avail1 = Availability(time: "5/4/22, 6:00 PM", userID: 0, ID: 1)

let Josh = User(name: "Josh", image: "profile.png", teaching: [MATH1120,CS2110],availability: [avail1], rate: "15", notifications: [notif1],email: "JS239@cornell.edu" ,ID: 1)

let notif1 = Notification(image: "profile.png", label: "kjc248 wants to learn from you",senderID: 0,receiverID: 1,ID: 0, time: "2022-05-06 03:17:18.934100")

let Joel = User(name: "Joel", image: "profile.png", teaching: [MATH1120,CS2110],availability: [avail1], rate: "15", notifications: [notif1], email: "jev66@cornell.edu",ID: 0)

let Lukman = User(name: "Lukman", image: "profile.png", teaching: [MATH1120,CS2110], availability: [avail1], rate: "15", notifications: [notif1], email: "lm264@cornell.edu", ID: 4)




extension Course: Equatable,Comparable {
    static func < (lhs: Course, rhs: Course) -> Bool {
        return lhs.getCourseNumber() < rhs.getCourseNumber()
    }
    
    static func == (lhs: Course, rhs: Course) -> Bool {
        return (lhs.code == rhs.code && lhs.tutors == rhs.tutors)
    }
}

extension User: Equatable {
    static func == (lhs: User, rhs: User) -> Bool {
        return
            lhs.id == rhs.id
    }
    
}

extension UIImageView {
    func load(url: URL) {
            DispatchQueue.global().async { [weak self] in
                if let data = try? Data(contentsOf: url) {
                    if let image = UIImage(data: data) {
                        DispatchQueue.main.async {
                            self?.image = image
                        }
                    }
                }
            }
        }
}
