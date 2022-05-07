//
//  NetworkManager.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/5/22.
//

import Foundation
import Alamofire

class NetworkManager {
    
    static let host = "http://34.130.13.109"
    
    
    // MARK: Course functions
    
    static func getAllCourses(completion: @escaping ([Course]) -> Void) {
        let endpoint = "\(host)/api/courses/"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode( [Course].self , from: data) {
                        completion(userResponse)
                    } else {
                        print("failed to decode getAllCourses")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func prepopulateCourses(completion: @escaping ([Course]) -> Void) {
        
        let endpoint = "\(host)/api/allcourses/"
        
        AF.request(endpoint, method: .post).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode([Course].self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to prepopulate courses")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func getCourse(courseCode: String, completion: @escaping (Course) -> Void){
        
        let endpoint = "\(host)/api/courses/\(courseCode)"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(Course.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("failed to decode getCourse")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func getCourseTutors(code: String, completion: @escaping ([User]) -> Void) {
        let endpoint = "\(host)/coursetutors/\(code)"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case .success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode([User].self, from: data) {
                        completion(userResponse)
                    } else {
                        print("failed to decode getCourseTutors")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func addTutor(courseID: String, userID: String, completion: @escaping (Course) -> Void){
        
        let endpoint = "\(host)/api/courses/\(courseID)/add/"
        let params: [String : String] = [
            "user_id": userID
        ]
        
        AF.request(endpoint, method: .post, parameters: params, encoder: JSONParameterEncoder.default).validate().responseData { response in switch response.result {
                case .success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(Course.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode addTutor")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
        
    }
    
    static func dropTutor(courseID: Int,UserID: Int, completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/api/courses/\(courseID)/drop/"
        let params: [String : String] = [
            "user_id": String(UserID)
        ]
        AF.request(endpoint, method: .post, parameters: params, encoder: JSONParameterEncoder.default).validate().responseData { response in
            switch response.result {
                case .success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("failed to decode dropTutor")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    // MARK: User methods and Login
    
    static func getUserData(userID: String, completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/api/users/\(userID)/"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("failed to decode getUserData")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func getCurrentUser(completion: @escaping (User) -> Void){
        
        let endpoint = "\(host)/api/users/current/"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode getCurrentUser")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func updateRate(userID: String, rate: String, completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/api/rate/\(userID)"
        let params: [String: String] = [
            "rate": rate
        ]
        
        AF.request(endpoint, method: .post, parameters: params,encoder: JSONParameterEncoder.default).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode updateRate")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
            
        }
    }
    
    static func LogIn(email: String, password: String, completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/login/"
        let params: [String : String] = [
            "email" : email,
            "password": password
        ]
        
        AF.request(endpoint, method: .post,parameters: params, encoder: JSONParameterEncoder.default).validate().responseData { response in
            switch response.result {
                case .success(let data) :
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode LogIn")
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    static func updateSession(update_token: String, completion: @escaping (User) -> Void) {
        
//        let endpoint = "\(host)/session/"
//        var headers: HTTPHeader =
//        [ "Authorization" : update_token ]
//
//        AF.request(endpoint, method: .get, headers: headers).validate().responseData {
//            _ in
//        }
        
        
        
        
        
        
//        AF.request(endpoint, method: .post, parameters: [:], encoder: JSONEncoder(), headers: headers).validate().responseData { response in
//            switch response.result {
//                case .success(let data) :
//                    let jsonDecoder = JSONDecoder()
//                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
//                        completion(userResponse)
//                    } else {
//                        print("Failed to decode updateSession")
//                    }
//                case .failure(let error):
//                    print(error.localizedDescription)
//            }
//        }
    }
    
    static func registerUser(email: String, password: String, name: String, profile_pic: String, completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/register/"
        let params: [String:String] = [
            "email" : email,
            "password" : password,
            "name" : name,
            "profile_pic" : profile_pic
        ]
        
        AF.request(endpoint, method: .post, parameters: params, encoder: JSONParameterEncoder.json).validate().responseData { response in
            switch response.result {
                case .success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode registerUser")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
        
    }
    
    static func verifySession(completion: @escaping (User) -> Void) {
        
        let endpoint = "\(host)/secret/"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case .success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(User.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode verifySession")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
                }
        }
    }
    
    
    // MARK: Availability Functions
    
    static func addAvailability (userID: Int,time: String, completion: @escaping (Availability) -> Void) {
        
        let endpoint = "\(host)/api/users/\(userID)/availability/"
        let params: [String : String] = [
            "time": time
        ]
        
        AF.request(endpoint, method: .post, parameters: params, encoder: JSONParameterEncoder.default).validate().responseData {
            response in switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(Availability.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode addAvailability")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
        
    }
    
    static func deleteAvailability (userID: Int, availID: Int, completion: @escaping (Availability) -> Void) {
        
        let endpoint = "\(host)/api/users/\(userID)/availability/\(availID)"
        AF.request(endpoint, method: .post).validate().responseData {
            response in switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(Availability.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode deleteAvailability")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    // MARK: Notification Functions
    
    static func getUserNotifications(userID: Int, completion: @escaping ([Notification]) -> Void) {
        
        let endpoint = "\(host)/api/users/notifications/\(userID)"
        
        AF.request(endpoint, method: .get).validate().responseData { response in
            switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode([Notification].self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode getUserNotifications")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
        
    }
    
    static func createNotification(senderID: Int, receiverID: Int, completion: @escaping (Notification) -> Void) {
        
        let endpoint = "\(host)/api/notifications/"
        let params: [String : String] = [
            "sender_id": String(senderID),
            "receiver_id": String(receiverID)
        ]
        
        AF.request(endpoint, method: .post, parameters: params, encoder: JSONParameterEncoder.default).validate().responseData {
            response in switch response.result {
                case.success(let data):
                    let jsonDecoder = JSONDecoder()
                    if let userResponse = try? jsonDecoder.decode(Notification.self, from: data) {
                        completion(userResponse)
                    } else {
                        print("Failed to decode createNotification")
                    }
                case.failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
}
